# Inventory Decision Adversarial Contracts

| Boundary | Adversarial case | Required outcome |
|---|---|---|
| record contract | required field missing or unknown field present | reject before loading |
| quantity contract | negative stock or zero/negative lead time | reject before policy |
| source loading | duplicate product identity | reject before cleaning |
| signal join | missing or unknown product key | reject before policy |
| unit compatibility | stock or signal unit differs from contract | reject before policy |
| canonical report | missing, corrupt or internally inconsistent | safe service error |
| freshness | evidence older than seven days | return `stale` warning, not fresh evidence |
| HTTP/client | validated report unavailable | `503` and no fallback recommendation |

These controls fail closed. They do not coerce incompatible evidence, invent a
lead time outside the versioned policy default, or publish a recommendation
from a corrupt artifact.
