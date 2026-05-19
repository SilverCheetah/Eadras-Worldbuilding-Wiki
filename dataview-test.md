```dataview
TABLE WITHOUT ID file.link AS "Page", file.mtime AS "Modified"
FROM "wiki"
SORT file.mtime DESC
LIMIT 10 
```