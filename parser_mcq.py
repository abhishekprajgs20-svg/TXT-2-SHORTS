"""MCQ .txt file parser â€” same logic as desktop app."""
import re


def clean_text(text):
    if not text: return ""
    t = re.sub(r'www\\.\\S+', '', text, flags=re.IGNORECASE)
    t = re.sub(r'@\\S+', '', t)
    t = re.sub(r'https?://\\S+', '', t)
    t = re.sub(r'pakexampoint[^\\n]*', '', t, flags=re.IGNORECASE)
    t = re.sub(r'PowerUp\\s+Prelims[^\\n]*', '', t, flags=re.IGNORECASE)
    t = re.sub(r'No part of this document[^\\n]*', '', t, flags=re.IGNORECASE)
    t = re.sub(r'[ \\t]+', ' ', t).strip()
    return t


def parse_mcq_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    raw_blocks = re.split(r'(?=\\bQ\\d+[\\.\\s\\:\\)])', content)
    questions  = []

    for block in raw_blocks:
        block = block.strip()
        if not block: continue
        hm = re.match(r'^Q(\\d+)[\\.\\s\\:\\)]\\s*(.*)', block, re.DOTALL)
        if not hm: continue
        q_num = int(hm[1])
        rest  = hm[2].strip()

        em = re.search(r'\\n\\s*(?:Ex|Explanation)\\s*:\\s*(.*)', rest, re.DOTALL | re.IGNORECASE)
        if em:
            q_and_opts  = rest[:em.start()].strip()
            explanation = em.group(1).strip()
        else:
            q_and_opts  = rest
            explanation = ""

        explanation = clean_text(explanation)
        lines = [l.strip() for l in q_and_opts.split('\\n') if l.strip()]
        lines = [l for l in lines if l not in ['ðŸ˜‚','ðŸ˜Š','ðŸ‘','ðŸ™']]

        opts, correct_idx = [], 0
        ans_m    = re.search(r'\\bAnsw\\s*er\\s*:\\s*([a-d])\\b', explanation, re.IGNORECASE)
        explicit = ord(ans_m.group(1).lower()) - ord('a') if ans_m else -1

        if len(lines) >= 5:
            possible = lines[-4:]; q_lines = lines[:-4]
            for i, ol in enumerate(possible):
                correct = ('âœ…' in ol) or (explicit == i)
                clean_o = ol.replace('âœ…','').strip()
                clean_o = re.sub(r'^(?:[a-dA-D][\\.\\)]|[1-4][\\.\\)])\\s*', '', clean_o).strip()
                opts.append(clean_text(clean_o))
                if correct: correct_idx = i
        else:
            q_lines = lines
            opts    = ["Option A", "Option B", "Option C", "Option D"]

        q_text = clean_text("\\n".join(q_lines).strip())
        first  = q_lines[0] if q_lines else f"Question {q_num}"
        title  = first[:50] + "..." if len(first) > 50 else first

        questions.append({
            "number": q_num, "title": title,
            "questionText": q_text, "options": opts,
            "correctIndex": correct_idx, "explanation": explanation
        })

    return questions