# Tests

Les tests du projet **Elegant-elegans** sont rédigés à l'aide de la bibliothèque `pytest`.
Chaque fichier du répertoire `tests` commence par le préfixe `test_` suivi du nom du répertoire plus le nom du fichier python au sein duquel les fonctions que l'on souhaite testées se trouvent. Par exemple, au sein du répertoire ***converter*** se trouve le fichier ***parser.py*** contenant un certain nombre de fonctions. L'ensemble des tests associées aux fonctions de ***parser.py*** sont rassemblés dans le fichier ***test_converter_parsing.py***.


## En bref
Chaque fonctions intervenant au sein d'une fonctionalité possède un ensemble de tests unitaires associé.
Pour exécuter l'ensemble des tests, l'utilisateur doit installer au préalable la bibliothèque `pytest` via la commande:
```bash
# conda environment
 conda install -c anaconda pytest
 # pip environment
pip install pytest
# poetry environment
poetry add pytest
```

Après avoir installé `pytest` vous pouvez exécuter, en vous situant à la racine du répertoire `Elegant-elevans`, l'ensemble des tests via la commande:
```bash
# conda environment
 pytest tests
 # pip environment
pytest tests
# poetry environment
poetry run pytest tests
```

Il est possible d'exécuter un ensemble de test spécifique à un fonctionalité via la commande:
```bash
# conda environment
 pytest tests.[tests filename].py
 # pip environment
pytest tests.[tests filename].py
# poetry environment
poetry run pytest tests.[tests filename].py

# example:
pytest tests.test_converter_parser.py
```

## Guide de rédaction d'un test:
La rédaction d'un test d'une fonction suit la procédure suivante:
* la fonction de test porte le même nom que la fonction testée et possède le préfixe `test_`
* la fonction de test est décorée par le décorateur `@pytest.mark.parametrize`
* `assert` (ou une de ses *variante*) est utilisé pour vérifier l'égalité entre le résultat obtenu et le résultat attendu.

Vous pouvez vous référer à la documentation de pytest ([ici](https://docs.pytest.org/en/7.1.x/) ou encore [là](https://docs.pytest.org/en/7.1.x/how-to/assert.html#assertraises) pour le contexte manager afin de tester les `raises` des fonctions).
