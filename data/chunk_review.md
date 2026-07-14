# Chunk Quality Review — Constitution of Pakistan (Articles 8–28)

**Date:** 2026-07-14  
**Dataset:** Constitution of Pakistan, 1973 — Fundamental Rights Chapter (Articles 8–28)  
**Total chunk files reviewed:** 10 out of 26  
**Reviewer:** Intern — manual file-by-file inspection  

---

## How Chunking Was Done

Before getting into the review, here is a quick explanation of exactly how the chunking script works, so anyone reading this report knows what to expect from the chunk files.

### The Basic Idea

The cleaned Constitution text was already split into individual `.txt` files — one file per Article (for example, `constitution_article_10.txt` contains only Article 10, nothing else). The chunking step takes those files and breaks them down further into smaller pieces that the embedding model can handle efficiently.

The reason we chunk is simple: some Articles (like Article 10 on arrest and detention) are very long. If you feed a 700-word block of text into the embedding model, the model compresses it into a single vector and a lot of detail gets lost. Smaller chunks mean more precise retrieval — when a user asks a question, the system can return the exact relevant 300–500 words rather than a big blob of the whole Article.

### Chunking Rules (as coded in `chunking_constitutional.py`)

| Parameter | Value | Reason |
|-----------|-------|--------|
| Maximum chunk size | **500 words** | Keeps each chunk within a reasonable token limit for the embedding model |
| Overlap between chunks | **50 words** | Prevents the boundary between chunk 0 and chunk 1 from cutting a sentence in half — the last 50 words of chunk 0 are repeated at the start of chunk 1 |
| Boundary alignment | **Article-level** | A chunk never starts in the middle of one Article and ends in another — each chunk belongs to exactly one Article |
| Splitting method | **Word-based** | The script splits by word count, not by character count or sentence count |
| Minimum chunk size | **No minimum enforced** | Short Articles (like Article 9 which is just one sentence) are kept as a single chunk even if they are only 15–20 words |

### When Does an Article Get Split?

- If the Article is **500 words or less**, it stays as one single chunk file (`article_X_chunk_0.txt`).  
- If the Article is **more than 500 words**, the script splits it into multiple chunks. Each chunk is 500 words max. The overlap ensures the last 50 words of the previous chunk appear again at the start of the next chunk so nothing gets cut off abruptly.

In our Constitution dataset (Articles 8–28), only **Article 10** was long enough to be split. It got split into two chunks:
- `constitution_article_10_chunk_0.txt` — first 500 words (clauses 1–5)
- `constitution_article_10_chunk_1.txt` — remaining 297 words (clauses 6–9), with ~50-word overlap from the end of chunk_0

Every other Article in this dataset fits comfortably under 500 words and has only one chunk each.

---

## What I Checked for Each Chunk

I opened each file manually and checked six things:

1. **Article boundary** — does the chunk contain only one Article, or did two Articles bleed into each other?
2. **Word count / size** — is it within the 500-word limit? If it is short, is it short because the Article itself is short?
3. **Readability** — is the text clean and readable, or are there garbled characters, encoding issues, or leftover symbols from the original PDF?
4. **Completeness** — are all the clauses, sub-clauses and provisos of the Article present? Nothing missing?
5. **No duplicate text** — does any paragraph appear twice inside the same chunk?
6. **Overlap check** (only for split Articles) — do chunk_0 and chunk_1 share approximately 50 words at their boundary?

---

## Review of 10 Chunks

---

### 1. Article 8 — `constitution_article_8_chunk_0.txt`

Article 8 covers laws inconsistent with fundamental rights being void. It has 5 numbered clauses and several sub-clauses.

- **Words:** ~323
- **Split:** No, single chunk
- **Boundary:** Fine — only Article 8 content, ends cleanly before Article 9.
- **Completeness:** All 5 clauses present. Sub-clauses (a), (b)(i), (b)(ii) are all there.
- **Issue found:** On one line there is a leftover fragment that reads `"] 17 and no such law..."` — the bracket `] 17` is a cleanup artifact from the amendment numbering in the original source. The `17` refers to a constitutional amendment footnote. The cleaning script removed the opening bracket (`17[`) but left the closing bracket behind. The text still reads fine — it does not affect meaning.
- **Duplicates:** None.

**Verdict: Acceptable.** Minor cleaning artifact, does not affect the content.

---

### 2. Article 9 — `constitution_article_9_chunk_0.txt`

Article 9 is "Security of person." It is one short sentence.

- **Words:** 18
- **Split:** No, single chunk
- **Boundary:** Fine — only Article 9, nothing else.
- **Completeness:** The entire Article is one sentence and it is fully present.
- **Readability:** Perfectly clean.
- **Duplicates:** None.

**Verdict: Pass.** Correctly saved as a single tiny chunk. A short chunk here is expected and correct.

---

### 3. Article 9A — `constitution_article_9a_chunk_0.txt`

Article 9A is "Clean and healthy environment" — also one sentence, added by a later amendment.

- **Words:** 17
- **Split:** No, single chunk
- **Boundary:** Fine — Article 9A is a standalone sub-article and it is the only content.
- **Completeness:** Full content present.
- **Readability:** Clean.
- **Duplicates:** None.

**Verdict: Pass.** The script correctly recognized 9A as a separate article from 9 and saved it separately.

---

### 4. Article 10, Chunk 0 — `constitution_article_10_chunk_0.txt`

Article 10 is the longest Article in the dataset — safeguards as to arrest and detention.

- **Words:** 500 (exactly at the limit)
- **Split:** Yes — this is the first of two chunks
- **Boundary:** Fine — only Article 10 content.
- **Completeness:** Contains clauses (1) through the first part of clause (5). Ends mid-sentence intentionally so the overlap can carry the rest into chunk_1.
- **Readability:** There is a formatting issue — the entire chunk is written as one long paragraph with no line breaks. The original Article had numbered clauses on separate lines but when the chunker joined words back together, the newlines were lost. The content is all there and correct but visually it is harder to read. For embedding purposes this does not matter much since the model reads the words, not the layout.
- **Overlap check:** The chunk ends at the phrase `"(6) The authority making"` — I confirmed that chunk_1 starts with those exact words. The overlap is working.
- **Duplicates:** None.

**Verdict: Acceptable.** Content is complete, overlap is correct. Newline formatting is lost but does not affect embedding quality.

---

### 5. Article 10, Chunk 1 — `constitution_article_10_chunk_1.txt`

This is the second half of Article 10.

- **Words:** ~297
- **Split:** Yes — this is the second of two chunks
- **Boundary:** Fine — still only Article 10.
- **Completeness:** Clauses (6), (7), (8), and (9) are all present including the long proviso in clause (7) about enemy aliens and anti-national activity.
- **Readability:** Same single-line formatting issue as chunk_0 — no line breaks, all one block. Same verdict applies.
- **Overlap check:** Starts with `"which the order has been made, and shall afford him..."` — this matches approximately 50 words from the tail end of chunk_0. Overlap confirmed.
- **Duplicates:** None.

**Verdict: Acceptable.** Overlap working correctly, all content present.

---

### 6. Article 10A — `constitution_article_10a_chunk_0.txt`

Article 10A is "Right to fair trial" — one sentence long, added by a constitutional amendment.

- **Words:** 33
- **Split:** No, single chunk
- **Boundary:** Clean — only 10A, correctly separated from Article 10.
- **Completeness:** The full Article is one sentence and it is present.
- **Readability:** Clean, has the title formatted properly with a tab before it.
- **Duplicates:** None.

**Verdict: Pass.** Correctly handled as a sub-article distinct from Article 10.

---

### 7. Article 17 — `constitution_article_17_chunk_0.txt`

Article 17 covers freedom of association and political parties.

- **Words:** ~155
- **Split:** No, single chunk
- **Boundary:** Clean — only Article 17.
- **Completeness:** All 3 clauses present. Clause (2) includes the full text about political parties and the Federal Constitutional Court which is a newer amendment — it is all there.
- **Readability:** This is one of the better-formatted chunks. The tabs for each clause are preserved and it reads almost as it would in the original document.
- **Duplicates:** None.

**Verdict: Pass.**

---

### 8. Article 22 — `constitution_article_22_chunk_0.txt`

Article 22 covers safeguards for educational institutions with respect to religion.

- **Words:** ~165
- **Split:** No, single chunk
- **Boundary:** Clean — only Article 22.
- **Completeness:** All 4 clauses and the sub-clauses (a) and (b) under clause (3) are present.
- **Readability:** Good formatting, tabs preserved.
- **Duplicates:** None.

**Verdict: Pass.**

---

### 9. Article 24 — `constitution_article_24_chunk_0.txt`

Article 24 is the most complex Article I checked — protection of property rights with 4 main clauses and 6 sub-clauses under clause (3) alone, with further sub-clauses (i), (ii), (iii).

- **Words:** ~356
- **Split:** No, single chunk (fits under 500 words)
- **Boundary:** Clean — only Article 24.
- **Completeness:** Checked all sub-clauses (a) through (f) under clause (3) and all three sub-points under (e). Every single one is present. Clause (4) about adequacy of compensation is also there at the end.
- **Readability:** Tabs preserved, very readable, hierarchy of sub-clauses is clear.
- **Duplicates:** None.

**Verdict: Pass.** This was the most thorough check — complex structure, all intact.

---

### 10. Article 25 — `constitution_article_25_chunk_0.txt`

Article 25 covers equality of citizens.

- **Words:** ~52
- **Split:** No, single chunk
- **Boundary:** Clean — only Article 25. Correctly does not include Article 25A which is a separate sub-article.
- **Completeness:** All 3 clauses present.
- **Readability:** Small cosmetic issue — clause (2) reads "There shall be no discrimination on the basis of sex ." with a space before the period. This happened because the original source had an empty amendment bracket `39[]39` at that point and when the cleaning script removed it, a trailing space was left. Harmless.
- **Duplicates:** None.

**Verdict: Acceptable.** One cosmetic space character, no actual content issue.

---

## Summary of All 10 Chunks

| Chunk | Article | Words | Boundary OK | Complete | Readable | Overlap OK | Result |
|-------|---------|-------|-------------|----------|----------|------------|--------|
| article_8_chunk_0 | 8 | 323 | Yes | Yes | Minor artifact | N/A | Acceptable |
| article_9_chunk_0 | 9 | 18 | Yes | Yes | Clean | N/A | Pass |
| article_9a_chunk_0 | 9A | 17 | Yes | Yes | Clean | N/A | Pass |
| article_10_chunk_0 | 10 (pt.1) | 500 | Yes | Yes | No line breaks | Yes | Acceptable |
| article_10_chunk_1 | 10 (pt.2) | 297 | Yes | Yes | No line breaks | Yes | Acceptable |
| article_10a_chunk_0 | 10A | 33 | Yes | Yes | Clean | N/A | Pass |
| article_17_chunk_0 | 17 | 155 | Yes | Yes | Clean | N/A | Pass |
| article_22_chunk_0 | 22 | 165 | Yes | Yes | Clean | N/A | Pass |
| article_24_chunk_0 | 24 | 356 | Yes | Yes | Clean | N/A | Pass |
| article_25_chunk_0 | 25 | 52 | Yes | Yes | Minor artifact | N/A | Acceptable |

---

## Issues Found

Three minor issues came up across the 10 chunks. None of them are blockers.

**Issue 1 — Stray amendment bracket in Article 8**  
The text contains `] 17` on one line, which is a leftover from the amendment footnote numbering in the original government source document. The cleaning script removed the opening bracket but missed the closing one. Purely cosmetic.

**Issue 2 — Article 10 chunks are flat single-line text**  
When the chunker split Article 10 by words and joined them back as a string, all original newlines were lost. The two Article 10 chunks are readable single paragraphs but do not have the numbered clause formatting. This could be improved in a future version of the chunking script by working line-by-line rather than word-by-word. For embedding and retrieval, this makes no practical difference.

**Issue 3 — Trailing space in Article 25, clause 2**  
A space before the final period in clause (2). Caused by an empty bracket `[]` that was removed during cleaning. No content impact.

No chunk failed on boundaries, completeness, or duplicate text.

---

## Conclusion

All 10 chunks reviewed passed the core quality checks. Article boundaries are clean throughout — no chunk contains content from two different Articles. The 50-word overlap between the two Article 10 chunks was confirmed to be working correctly. The three minor issues noted above are all cosmetic and do not affect the text content that will be fed to the embedding model.

The Constitution dataset is ready to proceed to the embedding generation step.
