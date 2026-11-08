# Поиск по библиографии статьи о Co3O4

[порождено: OpenAI Codex GPT-5] Черновик подготовлен Codex; пять интерпретаций выдачи требуют авторской проверки и переписывания перед сдачей. AI4Science/Goose для этого отчёта не запускался.

[источник] Библиографические DOI извлечены из `library/simonenko_et_al_2022_co3o4.pdf` (54 ссылки); метаданные OpenAlex получены по DOI 2026-10-23. В поисковую библиотеку вошли записи с доступной аннотацией: 31 документов. Единица поиска — название + аннотация, не полный текст статьи.

Коллекция ограничена аннотированными работами из списка литературы исходной статьи. Это не случайная выборка всех работ по Co3O4 и не рейтинг доказательности.

Сравнение: BM25 (k1=1.2, b=0.75) и векторный поиск TF-IDF → TruncatedSVD (16 латентных измерений) с cosine similarity. Векторная модель здесь является локальным учебным baseline, а не нейросетевым sentence-transformer. Оба метода работают на одинаковых title+abstract текстах.

## Запросы и результаты

### Запрос 1: chemical precipitation synthesis conditions pH thermal treatment Co3O4 nanopowder

| Ранг | BM25 | Векторный поиск |
|---:|---|---|
| 1 | [Effect of the precipitation pH on the characteristics and performance of Co3O4 catalysts in the total oxidation of toluene and propane](https://doi.org/10.1016/j.apcatb.2020.119566) (2020; W3088456678; 9.659) | [Preparation–Morphology–Performance Relationships in Cobalt Aerogels as Supercapacitors](https://doi.org/10.1021/am4047969) (2014; W2320528998; 0.664) |
| 2 | [Recent Advance in Co3O4 and Co3O4-Containing Electrode Materials for High-Performance Supercapacitors](https://doi.org/10.3390/molecules25020269) (2020; W3000683697; 9.611) | [Effect of the precipitation pH on the characteristics and performance of Co3O4 catalysts in the total oxidation of toluene and propane](https://doi.org/10.1016/j.apcatb.2020.119566) (2020; W3088456678; 0.640) |
| 3 | [Preparation of ZnS Nanopowders and Their Use in the Additive Production of Thick-Film Structures](https://doi.org/10.1134/S0036023621090126) (2021; W3200512257; 9.024) | [Recent Advance in Co3O4 and Co3O4-Containing Electrode Materials for High-Performance Supercapacitors](https://doi.org/10.3390/molecules25020269) (2020; W3000683697; 0.535) |
| 4 | [Synthesis, Characterization and Anti-Microbial Activity of Oxalate-Assisted CO3O4 Nanoparticles Derived from Homogeneous Co-Precipitation Method](https://doi.org/10.1142/S0219581X19500029) (2019; W2921444974; 6.198) | [Synthesis, Characterization and Anti-Microbial Activity of Oxalate-Assisted CO3O4 Nanoparticles Derived from Homogeneous Co-Precipitation Method](https://doi.org/10.1142/S0219581X19500029) (2019; W2921444974; 0.450) |
| 5 | [Synthesis and physicochemical properties of a solid oxide nanocomposite based on a ZrO2–Y2O3–Gd2O3–MgO system](https://doi.org/10.1134/S1087659616050060) (2016; W2525241005; 4.349) | [Features of Hydrothermal Growth of Hierarchical Co3O4 Coatings on Al2O3 Substrates](https://doi.org/10.1134/S0036023620090181) (2020; W3089107176; 0.440) |

[порождено: Codex GPT-5] Совпадение top-5: 3/5. BM25 ставит на первое место работу, где сама тема precipitation pH указана в заглавии; векторный поиск поднимает аэрогельную работу и обзор. Это полезно для широкой темы синтеза, но для точного протокола осаждения выдачу надо дополнительно сузить по экспериментальным условиям. Ранжирование — подсказка для чтения, а не проверка научной релевантности.

### Запрос 2: microplotter printing functional inks printed metal oxide structures

| Ранг | BM25 | Векторный поиск |
|---:|---|---|
| 1 | [A biofunctionalizable ink platform composed of catechol-modified chitosan and reduced graphene oxide/platinum nanocomposite](https://doi.org/10.3762/bjnano.8.151) (2017; W2738725804; 10.269) | [Programmable Contact Printing Using Ballpoint Pens with a Digital Plotter for Patterning Electrodes on Paper](https://doi.org/10.1021/acsomega.8b02592) (2018; W2904607923; 0.725) |
| 2 | [Freestanding Functional Structures by Aerosol‐Jet Printing for Stretchable Electronics and Sensing Applications](https://doi.org/10.1002/admt.201900048) (2019; W2921334366; 8.774) | [Freestanding Functional Structures by Aerosol‐Jet Printing for Stretchable Electronics and Sensing Applications](https://doi.org/10.1002/admt.201900048) (2019; W2921334366; 0.645) |
| 3 | [Programmable Contact Printing Using Ballpoint Pens with a Digital Plotter for Patterning Electrodes on Paper](https://doi.org/10.1021/acsomega.8b02592) (2018; W2904607923; 8.651) | [Platinum Based Nanoparticles Produced by a Pulsed Spark Discharge as a Promising Material for Gas Sensors](https://doi.org/10.3390/app11020526) (2021; W3120785707; 0.611) |
| 4 | [Platinum Based Nanoparticles Produced by a Pulsed Spark Discharge as a Promising Material for Gas Sensors](https://doi.org/10.3390/app11020526) (2021; W3120785707; 7.837) | [A biofunctionalizable ink platform composed of catechol-modified chitosan and reduced graphene oxide/platinum nanocomposite](https://doi.org/10.3762/bjnano.8.151) (2017; W2738725804; 0.493) |
| 5 | [Microplotter-Printed On-Chip Combinatorial Library of Ink-Derived Multiple Metal Oxides as an “Electronic Olfaction” Unit](https://doi.org/10.1021/acsami.0c14055) (2020; W3107413095; 6.227) | [Pen Plotter Printing of MnOx Thin Films Using Manganese Alkoxoacetylacetonate](https://doi.org/10.1134/S0036023621090138) (2021; W3200566241; 0.458) |

[порождено: Codex GPT-5] Совпадение top-5: 4/5. Запрос про микроплоттер и чернила не находит прямое совпадение в первых строках: BM25 выводит общие работы про печать/чернила, а статья с точным словом Microplotter появляется пятой. Векторный поиск предлагает смежные методы печати. Для проекта это пример, где точный термин и синонимы стоит искать отдельно. Ранжирование — подсказка для чтения, а не проверка научной релевантности.

### Запрос 3: printed Co3O4 perovskite solar cells screen printing

| Ранг | BM25 | Векторный поиск |
|---:|---|---|
| 1 | [Spinel Co 3 O 4 nanomaterials for efficient and stable large area carbon-based printed perovskite solar cells](https://doi.org/10.1039/c7nr08289d) (2017; W2778115116; 16.787) | [Spinel Co 3 O 4 nanomaterials for efficient and stable large area carbon-based printed perovskite solar cells](https://doi.org/10.1039/c7nr08289d) (2017; W2778115116; 0.970) |
| 2 | [Gas Sensing Properties of Co3O4-loaded SnO2 to Ethanol and Acetone](https://doi.org/10.1088/1674-0068/20/03/315-318) (2007; W1626875773; 6.324) | [Programmable Contact Printing Using Ballpoint Pens with a Digital Plotter for Patterning Electrodes on Paper](https://doi.org/10.1021/acsomega.8b02592) (2018; W2904607923; 0.412) |
| 3 | [Programmable Contact Printing Using Ballpoint Pens with a Digital Plotter for Patterning Electrodes on Paper](https://doi.org/10.1021/acsomega.8b02592) (2018; W2904607923; 5.087) | [Combinatorial optimization of spinel Co 3−x M x O 4 M = (Al, Ga, In) alloyed thin films prepared by ink jet printing: photoelectrochemical, optical, and structural properties](https://doi.org/10.1039/c4ta05671j) (2015; W2079221767; 0.276) |
| 4 | [Freestanding Functional Structures by Aerosol‐Jet Printing for Stretchable Electronics and Sensing Applications](https://doi.org/10.1002/admt.201900048) (2019; W2921334366; 3.629) | [Controllable synthesis of self-assembly Co 3 O 4 nanoflake microspheres for electrochemical performance](https://doi.org/10.1088/0957-4484/27/35/355603) (2016; W2482014493; 0.217) |
| 5 | [A biofunctionalizable ink platform composed of catechol-modified chitosan and reduced graphene oxide/platinum nanocomposite](https://doi.org/10.3762/bjnano.8.151) (2017; W2738725804; 3.432) | [Freestanding Functional Structures by Aerosol‐Jet Printing for Stretchable Electronics and Sensing Applications](https://doi.org/10.1002/admt.201900048) (2019; W2921334366; 0.201) |

[порождено: Codex GPT-5] Совпадение top-5: 3/5. Оба метода ставят на первое место одну и ту же работу о печатных перовскитных солнечных элементах с Co3O4. Это наиболее согласованная выдача из пяти; векторный score первого результата заметно выше остальных, а BM25 добавляет общие статьи о печати. Ранжирование — подсказка для чтения, а не проверка научной релевантности.

### Запрос 4: nanostructured Co3O4 morphology porous electrode supercapacitor

| Ранг | BM25 | Векторный поиск |
|---:|---|---|
| 1 | [MOF-templated syntheses of porous Co 3 O 4 hollow spheres and micro-flowers for enhanced performance in supercapacitors](https://doi.org/10.1039/C8CE00613J) (2018; W2805415602; 7.222) | [Preparation–Morphology–Performance Relationships in Cobalt Aerogels as Supercapacitors](https://doi.org/10.1021/am4047969) (2014; W2320528998; 0.723) |
| 2 | [Recent Advance in Co3O4 and Co3O4-Containing Electrode Materials for High-Performance Supercapacitors](https://doi.org/10.3390/molecules25020269) (2020; W3000683697; 6.056) | [Recent Advance in Co3O4 and Co3O4-Containing Electrode Materials for High-Performance Supercapacitors](https://doi.org/10.3390/molecules25020269) (2020; W3000683697; 0.675) |
| 3 | [Controllable synthesis of self-assembly Co 3 O 4 nanoflake microspheres for electrochemical performance](https://doi.org/10.1088/0957-4484/27/35/355603) (2016; W2482014493; 4.390) | [Controllable synthesis of self-assembly Co 3 O 4 nanoflake microspheres for electrochemical performance](https://doi.org/10.1088/0957-4484/27/35/355603) (2016; W2482014493; 0.626) |
| 4 | [Green Fabrication of Ultrathin Co3O4Nanosheets from Metal–Organic Framework for Robust High-Rate Supercapacitors](https://doi.org/10.1021/acsami.7b10309) (2017; W2767293566; 4.092) | [MOF-templated syntheses of porous Co 3 O 4 hollow spheres and micro-flowers for enhanced performance in supercapacitors](https://doi.org/10.1039/C8CE00613J) (2018; W2805415602; 0.599) |
| 5 | [Preparation–Morphology–Performance Relationships in Cobalt Aerogels as Supercapacitors](https://doi.org/10.1021/am4047969) (2014; W2320528998; 3.820) | [A low crystallinity oxygen-vacancy-rich Co 3 O 4 cathode for high-performance flexible asymmetric supercapacitors](https://doi.org/10.1039/c8ta06349d) (2018; W2884372257; 0.297) |

[порождено: Codex GPT-5] Совпадение top-5: 4/5. BM25 первым находит пористые Co3O4 hollow spheres, а векторный поиск начинает с аэрогелей и общего обзора электродов. Оба набора тематически подходят к морфологии и суперконденсаторам, но не взаимозаменяемы: лексическая модель точнее цепляется за porous, а векторная расширяет близкие материалы. Ранжирование — подсказка для чтения, а не проверка научной релевантности.

### Запрос 5: Co3O4 thin films deposition characterization optical electrical properties

| Ранг | BM25 | Векторный поиск |
|---:|---|---|
| 1 | [Structural, optical and electrical properties of Ni-doped Co3O4 prepared via Sol-Gel technique](https://doi.org/10.1590/1980-5373-mr-2017-0545) (2018; W2790605662; 10.241) | [Structural, optical and electrical properties of Ni-doped Co3O4 prepared via Sol-Gel technique](https://doi.org/10.1590/1980-5373-mr-2017-0545) (2018; W2790605662; 0.713) |
| 2 | [Characterization of Mn-Doped Co 3 O 4 Thin Films Prepared by Sol Gel-Based Dip-Coating Process](https://doi.org/10.1515/htmp-2017-0185) (2018; W2892680375; 9.604) | [Characterization of Mn-Doped Co 3 O 4 Thin Films Prepared by Sol Gel-Based Dip-Coating Process](https://doi.org/10.1515/htmp-2017-0185) (2018; W2892680375; 0.685) |
| 3 | [Pen Plotter Printing of MnOx Thin Films Using Manganese Alkoxoacetylacetonate](https://doi.org/10.1134/S0036023621090138) (2021; W3200566241; 8.745) | [Characterization of atomic layer deposited semiconducting Co3O4](https://doi.org/10.1116/1.5064469) (2019; W2909357423; 0.579) |
| 4 | [Characterization of atomic layer deposited semiconducting Co3O4](https://doi.org/10.1116/1.5064469) (2019; W2909357423; 8.075) | [Engineering Co Vacancies for Tuning Electrical Properties of p-Type Semiconducting Co 3 O 4 Films](https://doi.org/10.1021/acsami.1c05748) (2021; W3165657262; 0.563) |
| 5 | [Combinatorial optimization of spinel Co 3−x M x O 4 M = (Al, Ga, In) alloyed thin films prepared by ink jet printing: photoelectrochemical, optical, and structural properties](https://doi.org/10.1039/c4ta05671j) (2015; W2079221767; 8.044) | [Combinatorial optimization of spinel Co 3−x M x O 4 M = (Al, Ga, In) alloyed thin films prepared by ink jet printing: photoelectrochemical, optical, and structural properties](https://doi.org/10.1039/c4ta05671j) (2015; W2079221767; 0.489) |

[порождено: Codex GPT-5] Совпадение top-5: 4/5. Две модели согласны по первым двум работам о тонких плёнках и их свойствах. Ниже BM25 точнее отражает слова deposition/printing, а векторный поиск находит ALD-характеризацию и электрические свойства плёнок Co3O4. Здесь выдачи дополняют друг друга. Ранжирование — подсказка для чтения, а не проверка научной релевантности.

## Ограничения и происхождение

- Аннотации и метаданные получены из OpenAlex по DOI, извлечённым из исходной статьи; полный список с DOI и статусами OA находится в `pdf_availability.csv`.
- OpenAlex показал 31 аннотацию из 54 DOI. По нескольким DOI OpenAlex не вернул аннотацию; эти записи не включены в ранжируемую коллекцию.
- Не все OA-ссылки удалось получить как файл PDF напрямую: часть сайтов ответила 403 или HTML. В библиотеку добавлена одна проверенная PDF-копия с лицензией CC BY; другие ссылки и статусы записаны в `pdf_availability.csv` и `pdf_sources.md`.
- Качественные выводы по выдаче — предварительная ручная интерпретация, не экспертная оценка полноты литературы.
