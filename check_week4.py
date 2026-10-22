#!/usr/bin/env python3
"""
Проверка онтологии недели 4: иерархия, типы, экземпляры, заметки, задачи.

Usage:
    py -3 check_week4.py [--strict]

Exit code 0 — всё ОК, 1 — ошибки.
"""

import argparse
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
ONTOLOGY_YAML = ROOT / "ontology.yaml"
NOTES_DIR = ROOT / "ontology" / "notes"
OBSIDIAN_DIR = ROOT / ".obsidian"
TASKS_DIR = ROOT / "tasks"


def load_ontology():
    if not ONTOLOGY_YAML.exists():
        print(f"FAIL: {ONTOLOGY_YAML} не найден")
        sys.exit(1)
    with open(ONTOLOGY_YAML, encoding="utf-8") as f:
        return yaml.safe_load(f)


def check_hierarchy(data):
    """Проверка иерархии классов и отсутствие циклов."""
    classes = data.get("classes", {})
    class_names = set(classes.keys())

    # 1. ≥ 3 класса
    if len(class_names) < 3:
        print(f"FAIL: классов {len(class_names)} < 3")
        return False

    # 2. Проверка parent-ссылок
    for name, info in classes.items():
        parent = info.get("parent")
        if parent is not None and parent not in class_names:
            print(f"FAIL: класс {name} ссылается на несуществующий parent {parent}")
            return False

    # 3. Проверка циклов (BFS от каждого корня)
    roots = [n for n, c in classes.items() if c.get("parent") is None]
    if not roots:
        print("FAIL: нет корневого класса (parent=null)")
        return False

    visited = set()
    queue = list(roots)
    while queue:
        node = queue.pop(0)
        if node in visited:
            print(f"FAIL: обнаружен цикл в иерархии (повторный визит {node})")
            return False
        visited.add(node)
        for n, c in classes.items():
            if c.get("parent") == node and n not in visited:
                queue.append(n)

    # Все классы должны быть достижимы из корня
    if len(visited) != len(class_names):
        print(f"FAIL: не все классы достижимы из корня ({len(visited)}/{len(class_names)})")
        return False

    print(f"OK: иерархия {len(class_names)} классов, без циклов")
    return True


def check_relations(data):
    """Проверка domain/range отношений."""
    classes = set(data.get("classes", {}).keys())
    relations = data.get("relations", {})

    for rname, rinfo in relations.items():
        domain = rinfo.get("domain")
        range_cls = rinfo.get("range")
        if domain not in classes:
            print(f"FAIL: relation {rname} domain '{domain}' не в классах")
            return False
        if range_cls not in classes:
            print(f"FAIL: relation {rname} range '{range_cls}' не в классах")
            return False

    print(f"OK: {len(relations)} отношений, все domain/range согласованы")
    return True


def check_concepts(data):
    """Проверка экземпляров: ≥ 10, каждый с instance_of."""
    concepts = data.get("concepts", {})
    classes = set(data.get("classes", {}).keys())

    instances = [c for c, info in concepts.items() if info.get("kind") == "instance"]
    if len(instances) < 10:
        print(f"FAIL: экземпляров {len(instances)} < 10")
        return False

    for inst in instances:
        info = concepts[inst]
        instance_of = info.get("instance_of")
        if instance_of not in classes:
            print(f"FAIL: экземпляр {inst} instance_of='{instance_of}' не в классах")
            return False
        note_path = NOTES_DIR / f"Экземпляр_{inst}.md"
        if not note_path.is_file():
            print(f"FAIL: нет заметки экземпляра {inst}")
            return False
        parsed = read_frontmatter(note_path)
        if not parsed:
            print(f"FAIL: неверный frontmatter экземпляра {inst}")
            return False
        frontmatter, body = parsed
        if frontmatter.get("type") != "instance":
            print(f"FAIL: {note_path.name} не помечен type: instance")
            return False
        if frontmatter.get("instance_of") != f"Класс_{instance_of}":
            print(f"FAIL: {note_path.name} не ссылается на класс {instance_of}")
            return False
        if f"[[Класс_{instance_of}]]" not in body:
            print(f"FAIL: {note_path.name} не содержит wikilink на свой класс")
            return False
        if info.get("path") and not (ROOT / info["path"]).is_file():
            print(f"FAIL: файл экземпляра {inst} не найден: {info['path']}")
            return False

    print(f"OK: {len(instances)} экземпляров, все с instance_of")
    return True


def read_frontmatter(path):
    """Load YAML frontmatter and body from an Obsidian Markdown note."""
    try:
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---\n"):
            return None
        _, metadata, body = content.split("---", 2)
        return yaml.safe_load(metadata) or {}, body
    except (OSError, ValueError, yaml.YAMLError):
        return None


def note_class(path):
    parsed = read_frontmatter(path)
    if not parsed:
        return None, ""
    metadata, body = parsed
    instance_of = metadata.get("instance_of", "")
    if metadata.get("type") != "instance" or not instance_of.startswith("Класс_"):
        return None, body
    return instance_of.removeprefix("Класс_"), body


def is_subclass(classes, child, parent):
    seen = set()
    while child in classes and child not in seen:
        if child == parent:
            return True
        seen.add(child)
        child = classes[child].get("parent")
    return False


def check_graph_edges(data):
    """Validate each asserted graph edge against relation domain and range."""
    classes = data.get("classes", {})
    relations = data.get("relations", {})
    edges = data.get("graph_edges", [])
    if len(edges) < 10:
        print(f"FAIL: graph_edges содержит {len(edges)} рёбер, нужно не менее 10")
        return False

    for edge in edges:
        subject_path = ROOT / edge.get("subject", "")
        object_path = ROOT / edge.get("object", "")
        predicate = edge.get("predicate")
        relation = relations.get(predicate)
        if not subject_path.is_file() or not object_path.is_file() or not relation:
            print(f"FAIL: неполное ребро графа: {edge}")
            return False

        subject_class, subject_body = note_class(subject_path)
        object_class, _ = note_class(object_path)
        if not subject_class or not object_class:
            print(f"FAIL: конец ребра не является типизированным экземпляром: {edge}")
            return False
        if not is_subclass(classes, subject_class, relation.get("domain")):
            print(f"FAIL: {subject_path.name} несовместим с domain у {predicate}")
            return False
        if not is_subclass(classes, object_class, relation.get("range")):
            print(f"FAIL: {object_path.name} несовместим с range у {predicate}")
            return False

        target_link = f"[[{object_path.stem}]]"
        if target_link not in subject_body or predicate not in subject_body:
            print(f"FAIL: заметка {subject_path.name} не фиксирует ребро {predicate} к {object_path.name}")
            return False

    print(f"OK: {len(edges)} рёбер согласованы с domain/range и типами экземпляров")
    return True


def check_rules(data):
    """Проверка правил: ≥ 2."""
    rules = data.get("rules", {})
    if len(rules) < 2:
        print(f"FAIL: правил {len(rules)} < 2")
        return False
    if not {"правило_4", "правило_5"}.issubset(rules):
        print("FAIL: отсутствуют правила вывода выполненной задачи или блокировки родителя")
        return False
    print(f"OK: {len(rules)} правил")
    return True


def check_notes(data):
    """Проверка frontmatter и покрытия классов, экземпляров и отношений заметками."""
    if not NOTES_DIR.exists():
        print(f"FAIL: {NOTES_DIR} не существует")
        return False

    notes = list(NOTES_DIR.glob("*.md"))
    if not notes:
        print("FAIL: нет заметок в ontology/notes/")
        return False

    class_notes = [n for n in notes if n.name.startswith("Класс_")]
    instance_notes = [n for n in notes if n.name.startswith("Экземпляр_")]
    relation_notes = [n for n in notes if n.name.startswith("Отношение_")]

    if len(class_notes) < 3:
        print(f"FAIL: заметок классов {len(class_notes)} < 3")
        return False

    if len(instance_notes) < 10:
        print(f"FAIL: заметок экземпляров {len(instance_notes)} < 10")
        return False

    expected_classes = {f"Класс_{name}.md" for name in data.get("classes", {})}
    expected_relations = {f"Отношение_{name}.md" for name in data.get("relations", {})}
    if expected_classes != {n.name for n in class_notes}:
        print("FAIL: заметки классов не совпадают с классами ontology.yaml")
        return False
    if expected_relations != {n.name for n in relation_notes}:
        print("FAIL: заметки отношений не совпадают с relations ontology.yaml")
        return False

    # Проверка frontmatter (пропускаем legacy notes.md)
    for note in notes:
        if note.name == "notes.md":
            continue
        with open(note, encoding="utf-8") as f:
            first_line = f.readline().strip()
        if first_line != "---":
            print(f"FAIL: {note.name} не начинается с YAML frontmatter")
            return False

    for note in class_notes:
        metadata, _ = read_frontmatter(note)
        if not metadata or metadata.get("type") != "class":
            print(f"FAIL: неверный type у заметки класса {note.name}")
            return False
    for note in relation_notes:
        metadata, _ = read_frontmatter(note)
        name = note.stem.removeprefix("Отношение_")
        expected = data["relations"][name]
        if not metadata or metadata.get("type") != "relation":
            print(f"FAIL: неверный type у заметки отношения {note.name}")
            return False
        if metadata.get("domain") != expected.get("domain") or metadata.get("range") != expected.get("range"):
            print(f"FAIL: domain/range заметки {note.name} расходится с ontology.yaml")
            return False

    print(f"OK: {len(class_notes)} заметок классов, {len(instance_notes)} экземпляров, {len(relation_notes)} отношений")
    return True


def check_wikilinks_classes(data):
    """Проверка, что заметки классов содержат wikilinks на другие классы."""
    classes = set(data.get("classes", {}).keys())
    class_note_names = {f"Класс_{c}" for c in classes}

    for note_path in NOTES_DIR.glob("Класс_*.md"):
        with open(note_path, encoding="utf-8") as f:
            content = f.read()
        # Проверяем наличие хотя бы одного wikilink на класс
        found = False
        for cls in classes:
            if f"[[Класс_{cls}]]" in content:
                found = True
                break
        if not found:
            print(f"FAIL: {note_path.name} не содержит wikilink на класс")
            return False

    print("OK: заметки классов содержат wikilinks")
    return True


def check_relation_types(data):
    """Проверка типов концов всех отношений."""
    relations = data.get("relations", {})
    for rname, rinfo in relations.items():
        domain = rinfo.get("domain")
        range_cls = rinfo.get("range")
        if not domain or not range_cls:
            print(f"FAIL: relation {rname} не имеет domain или range")
            return False
        if not isinstance(domain, str) or not isinstance(range_cls, str):
            print(f"FAIL: relation {rname} domain/range не строка")
            return False
    print("OK: все отношения имеют строковые domain/range")
    return True


def check_tasks(data):
    """Проверка задач: статусы, outcome, outcome_file."""
    if not TASKS_DIR.exists():
        print(f"FAIL: {TASKS_DIR} не существует")
        return False

    task_files = list(TASKS_DIR.glob("*.md"))
    if not task_files:
        print("FAIL: нет файлов задач в tasks/")
        return False

    for tf in task_files:
        with open(tf, encoding="utf-8") as f:
            content = f.read()

        # Парсим YAML frontmatter вручную (простой парсер)
        if not content.startswith("---"):
            print(f"FAIL: {tf.name} не начинается с frontmatter")
            return False

        parts = content.split("---")
        if len(parts) < 3:
            print(f"FAIL: {tf.name} нет закрывающего ---")
            return False

        try:
            fm = yaml.safe_load(parts[1])
        except yaml.YAMLError as e:
            print(f"FAIL: {tf.name} невалидный YAML frontmatter: {e}")
            return False

        status = fm.get("status", "")
        valid_statuses = data["attributes"]["status"]["values"]
        if status not in valid_statuses:
            print(f"FAIL: {tf.name} статус '{status}' не в допустимых")
            return False

        # Для завершённых задач — outcome и outcome_file
        if status in ("выполнена", "принята"):
            if not fm.get("outcome"):
                print(f"FAIL: {tf.name} статус '{status}' без outcome")
                return False
            if not fm.get("outcome_file"):
                print(f"FAIL: {tf.name} статус '{status}' без outcome_file")
                return False
            if not (ROOT / fm["outcome_file"]).is_file():
                print(f"FAIL: {tf.name} файл результата не найден: {fm['outcome_file']}")
                return False
            if fm.get("inferred_class") != "Класс_ВыполненнаяЗадача":
                print(f"FAIL: {tf.name} не отмечен выводимым классом ВыполненнаяЗадача")
                return False

    print(f"OK: {len(task_files)} задач, статусы и итоги проверены")
    return True


def check_obsidian():
    """Проверка наличия .obsidian/."""
    if not OBSIDIAN_DIR.exists():
        print(f"FAIL: {OBSIDIAN_DIR} не существует")
        return False
    files = list(OBSIDIAN_DIR.iterdir())
    if not files:
        print("FAIL: .obsidian/ пуст")
        return False
    print(f"OK: .obsidian/ содержит {len(files)} файлов")
    return True


def main():
    parser = argparse.ArgumentParser(description="Проверка онтологии недели 4")
    parser.add_argument("--strict", action="store_true", help="Строгий режим")
    args = parser.parse_args()

    print("=" * 60)
    print("Проверка онтологии недели 4")
    print("=" * 60)

    data = load_ontology()
    all_ok = True

    checks = [
        ("Иерархия и циклы", check_hierarchy),
        ("Отношения domain/range", check_relations),
        ("Экземпляры (≥10)", check_concepts),
        ("Правила (≥2)", check_rules),
        ("Заметки классов/экземпляров", check_notes),
        ("Wikilinks классов", check_wikilinks_classes),
        ("Типы концов отношений", check_relation_types),
        ("Типизированные рёбра графа", check_graph_edges),
        ("Задачи: статусы и итоги", check_tasks),
        (".obsidian/ структура", check_obsidian),
    ]

    for name, fn in checks:
        try:
            # Функции с аргументом data получают data, без — вызываются без аргументов
            import inspect
            sig = inspect.signature(fn)
            if "data" in sig.parameters:
                ok = fn(data)
            else:
                ok = fn()
        except Exception as e:
            print(f"FAIL: {name} — исключение: {e}")
            ok = False
        if not ok:
            all_ok = False

    print("=" * 60)
    if all_ok:
        print("ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ — принято")
        sys.exit(0)
    else:
        print("ЕСТЬ ОШИБКИ")
        sys.exit(1)


if __name__ == "__main__":
    main()
