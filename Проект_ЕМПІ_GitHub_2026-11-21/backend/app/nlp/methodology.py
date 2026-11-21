"""Published scoring specification shared by the API and the worker."""

ALGORITHM_VERSION = "2.0.0"

SOURCES = [
    {
        "title": "Reimers and Gurevych 2019 — Sentence-BERT",
        "url": "https://aclanthology.org/D19-1410/",
        "supports": "Векторні представлення речень і семантичне порівняння косинусною подібністю.",
    },
    {
        "title": "Sentence Transformers — Semantic Textual Similarity",
        "url": "https://www.sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html",
        "supports": "Обчислення embeddings і косинусної подібності між усіма парами текстів.",
    },
    {
        "title": "Manning, Raghavan and Schütze 2008 — Introduction to Information Retrieval",
        "url": "https://nlp.stanford.edu/IR-book/html/htmledition/near-duplicates-and-shingling-1.html",
        "supports": "Коефіцієнт Жаккара як відношення потужності перетину множин до їх об’єднання.",
    },
    {
        "title": "Qi et al. 2020 — Stanza",
        "url": "https://aclanthology.org/2020.acl-demos.14/",
        "supports": "Токенізація, лематизація та визначення частин мови для нормалізації українського тексту.",
    },
    {
        "title": "Model card — paraphrase-multilingual-mpnet-base-v2",
        "url": "https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
        "supports": "Фактично використана багатомовна модель і її 768-вимірні представлення.",
    },
]

FORMULAS = [
    {
        "name": "Семантична подібність",
        "formula": "S_j = clip((u · v_j) / (||u|| · ||v_j||), 0, 1)",
        "description": "u — embedding відповіді, v_j — embedding еталона або затвердженої варіації. "
        "Для нульового вектора результат 0. Від’ємні значення косинуса обмежуються нулем.",
        "origin": "Косинусна подібність із Sentence-BERT та Sentence Transformers; clip — правило проєкту.",
    },
    {
        "name": "Лексична подібність",
        "formula": "L_j = |A ∩ R_j| / |A ∪ R_j|",
        "description": "A і R_j — множини лем змістових слів відповіді й кандидата. "
        "Службові частини мови та пунктуація відсіюються; заперечення зберігаються. "
        "Для порожнього об’єднання результат 0.",
        "origin": "Коефіцієнт Жаккара; лематизація виконується Stanza.",
    },
    {
        "name": "Покриття ключових понять",
        "formula": "C_j = Σ(w_i · I_i) / Σ(w_i)",
        "description": "I_i = 1, якщо знайдено поняття або заданий викладачем синонім як послідовність "
        "лем або точних словоформ; інакше 0. Точна словоформа захищає від неоднозначності лематизації. "
        "w_i — вага поняття. Без понять C_j не обчислюється.",
        "origin": "Власна зважена рубрика проєкту. Це не окрема формула оцінювання з публікації SBERT.",
    },
    {
        "name": "Індекс відповідності одному еталону",
        "formula": "F_j = a·S_j + b·L_j + c·C_j; якщо понять немає: F_j = (a·S_j + b·L_j)/(a+b)",
        "description": "a+b+c = 1. Початкові ваги 0.72, 0.08, 0.20; "
        "у розрахунку використовуються збережені налаштування конкретного аналізу.",
        "origin": "Власна гібридна схема проєкту на основі зваженого середнього. "
        "Ваги й пороги є налаштуваннями та потребують калібрування викладачем.",
    },
    {
        "name": "Вибір серед кількох еталонів",
        "formula": "j* = argmax_j F_j; F = F_j*",
        "description": "Повний F_j обчислюється окремо для кожного еталона та затвердженої варіації. "
        "За однакових F_j перевага у більшого S_j, потім L_j. Порівняння зберігаються в історії. "
        "Критичні правила з усіх еталонів питання застосовуються до кожного кандидата, "
        "щоб суперечність не можна було обійти вибором іншого еталона.",
        "origin": "Правило агрегації проєкту. Вибирається найкращий повний індекс, а не лише найбільший косинус.",
    },
]
