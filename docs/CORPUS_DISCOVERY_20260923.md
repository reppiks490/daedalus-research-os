# Local corpus discovery (CA, 2026-09-23)

The original archive's `artifacts/catalog_summary.json` covers only 238
chart CSVs. The owner's newer GitHub equity-candidate batches plus five local
chart-data directories are broader. This is an **inventory**, not validation
of chart provenance, tradeability, or a protected holdout.

Run `daedalus catalog` with these six source roots (as separate arguments):

1. `C:/Users/tripl/Downloads/Full csv candles only` — 238 real CSVs
2. `C:/Users/tripl/Downloads/Csv` — 144
3. `C:/Users/tripl/Downloads/Csv files for different chart types` — 124
4. `C:/Users/tripl/Downloads/More csv by ticks with chart candle and volume profiles technicals built in` — 87
5. `C:/Users/tripl/Downloads/Csv indexes` — 33
6. `C:/Users/tripl/Icarus-ml-d9d4db8/history/unzipped/candidates` — 177 stock-candidate CSVs from `multi-level-csv`'s six new batches

The combined catalog reports **803 source records, 542 unique SHA-256 hashes,
515 records in exact-byte duplicate groups, and 519 mechanics signatures**.
Every physical file retains its own catalog row; hash equality permits shared
compute only. Similar names do not imply duplicates. Longer historical
coverage and TPO, footprint, Renko, Heikin Ashi, session-profile or other
chart constructions remain distinct until their representation identity is
verified. The 177 stock files are contextual research sources, **not** NQ
execution bars.

Cataloging all of `Downloads` is inappropriate: it includes an empty unrelated
paper-orders CSV and the command fails on that file instead of silently
discarding it. The six-root catalog is local under ignored
`artifacts/catalog_six_roots.csv` because it contains absolute owner paths.
The owner must still verify source identity, timestamp units, chart settings,
data history and execution-safe anchors before model selection or protected
evaluation. No corpus holdout was spent by this inventory.
