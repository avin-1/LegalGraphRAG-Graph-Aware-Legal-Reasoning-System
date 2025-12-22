"""
Legal Graph Schema (conceptual)

Nodes:
- Statute {id, title, section}
- Case {id, court, year}
- Judge {name}

Edges:
- (:Case)-[:CITES]->(:Case)
- (:Case)-[:INTERPRETS]->(:Statute)
- (:Case)-[:DECIDED_BY]->(:Judge)
- (:Case)-[:OVERRULED_BY]->(:Case)
"""

