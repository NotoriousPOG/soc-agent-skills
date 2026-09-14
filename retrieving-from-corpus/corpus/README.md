# Corpus space

Drop operator-owned runbooks, detection notes, and past-incident write-ups
here (`.md`, `.txt`, `.json`). Then:

```bash
python ../scripts/index_corpus.py --corpus . --db index.sqlite
python ../scripts/query_corpus.py --db index.sqlite --q "your question"
```

Do not put lure samples, malware bytes, or secrets in this directory.
`index.sqlite` is gitignored.

`example/` is a tiny demo corpus used by tests. Replace it with your own.
