# Page snapshot

```yaml
- generic [ref=e4]:
  - banner [ref=e5]:
    - link "Retour au chat" [ref=e7] [cursor=pointer]:
      - /url: /
      - button "Retour au chat" [ref=e8] [cursor=pointer]:
        - img [ref=e9] [cursor=pointer]
        - text: Retour au chat
  - generic [ref=e11]:
    - generic [ref=e12]:
      - heading "Recherche dans la base" [level=1] [ref=e13]
      - paragraph [ref=e14]: Recherchez dans les bases Vidal et Meddispar
    - generic [ref=e16]:
      - generic [ref=e17]:
        - textbox "Rechercher un médicament, une maladie..." [ref=e18]: paracétamol
        - button "Rechercher" [disabled]:
          - img
          - text: Rechercher
      - generic [ref=e19]:
        - button "Toutes les sources" [ref=e20] [cursor=pointer]
        - button "Vidal" [ref=e21] [cursor=pointer]
        - button "Meddispar" [ref=e22] [cursor=pointer]
    - generic [ref=e23]:
      - img [ref=e24]
      - paragraph [ref=e26]: Recherche en cours...
```