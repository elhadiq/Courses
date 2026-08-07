# comprehension.xml — questions Moodle standards (SANS plugin)

Un `comprehension.xml` = `<quiz>` avec une question `category` puis 5–7 questions de types
`multichoice`, `truefalse`, `numerical`. Ces types s'importent dans n'importe quel Moodle
(pas besoin du plugin CodeRunner). Règles :

- Le **nom** (`<name><text>...`) et les **feedback** ne sont PAS en CDATA → n'y mettre que des
  entités XML valides (`&amp; &lt; &gt;`). Utiliser le vrai caractère « — » (U+2014), jamais `&mdash;`.
- Le **questiontext** et le **generalfeedback** sont en CDATA → HTML libre autorisé.
- Chaque question doit avoir une réponse à `fraction="100"`.
- Toujours démarrer par une question `category` pour ranger la banque proprement.

## En-tête de catégorie
```xml
<question type="category">
  <category><text>$course$/Nom du cours/Section N - Titre (Compréhension)</text></category>
</question>
```

## Choix multiple (une bonne réponse)
```xml
<question type="multichoice">
  <name><text>S1 C1 — Titre</text></name>
  <questiontext format="html"><text><![CDATA[<p>Question ?</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Explication.</p>]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>0.3333333</penalty>
  <hidden>0</hidden>
  <single>true</single>
  <shuffleanswers>true</shuffleanswers>
  <answernumbering>abc</answernumbering>
  <correctfeedback format="html"><text>Correct.</text></correctfeedback>
  <partiallycorrectfeedback format="html"><text>Partiellement correct.</text></partiallycorrectfeedback>
  <incorrectfeedback format="html"><text>Revoir la leçon.</text></incorrectfeedback>
  <answer fraction="100" format="html"><text><![CDATA[Bonne réponse]]></text><feedback format="html"><text>Correct.</text></feedback></answer>
  <answer fraction="0" format="html"><text><![CDATA[Distracteur]]></text><feedback format="html"><text>Non.</text></feedback></answer>
</question>
```

## Vrai / Faux
```xml
<question type="truefalse">
  <name><text>S1 C2 — Titre</text></name>
  <questiontext format="html"><text><![CDATA[<p>Affirmation.</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Explication.</p>]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>1.0000000</penalty>
  <hidden>0</hidden>
  <answer fraction="100" format="moodle_auto_format"><text>true</text><feedback format="html"><text>Correct.</text></feedback></answer>
  <answer fraction="0" format="moodle_auto_format"><text>false</text><feedback format="html"><text>Incorrect.</text></feedback></answer>
</question>
```
(Pour une affirmation FAUSSE, inverser les `fraction`.)

## Numérique
```xml
<question type="numerical">
  <name><text>S1 C3 — Titre</text></name>
  <questiontext format="html"><text><![CDATA[<p>Combien vaut ... ?</p>]]></text></questiontext>
  <generalfeedback format="html"><text><![CDATA[<p>Calcul.</p>]]></text></generalfeedback>
  <defaultgrade>1.0000000</defaultgrade>
  <penalty>0.3333333</penalty>
  <hidden>0</hidden>
  <answer fraction="100" format="moodle_auto_format"><text>42</text><feedback format="html"><text>Correct.</text></feedback><tolerance>0</tolerance></answer>
</question>
```

## Vérification
```python
import xml.etree.ElementTree as ET
root = ET.parse("comprehension.xml").getroot()
qs = [q for q in root.findall('question') if q.get('type') != 'category']
assert all('100' in [a.get('fraction') for a in q.findall('answer')] for q in qs)
```
