# -*- coding: utf-8 -*-
"""Build driver: emits every chapter folder, the exercise sheets and the index,
then self-tests every reference solution."""
import contextlib
import importlib
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import build_coderunner, build_stack  # noqa: E402
import site_pages as S  # noqa: E402

ROOT = '/sessions/admiring-intelligent-knuth/mnt/Quantum'
MODULES = [f'ch{i:02d}' for i in range(1, 11)]


def run_solution_tests(ch):
    failures = []
    for q in ch['coderunner']:
        for k, tc in enumerate(q['tests'], 1):
            g, buf = {}, io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    exec(q['answer'], g)
                    exec(tc['code'], g)
            except Exception as e:  # noqa: BLE001
                failures.append(f"{q['name']} tc{k}: {type(e).__name__}: {e}")
                continue
            if buf.getvalue() != tc['expected']:
                failures.append(f"{q['name']} tc{k}: got {buf.getvalue()!r} "
                                f"expected {tc['expected']!r}")
    return failures


def main():
    chapters, all_fail = [], []
    for m in MODULES:
        mod = importlib.import_module(m)
        ch = mod.CHAPTER
        all_fail += run_solution_tests(ch)
        chapters.append(ch)

    # first pass: render the body so figures can be counted for the index
    for ch in chapters:
        blob = '\n'.join(sec for _, sec in ch['sections'])
        ch['_figures'] = len(re.findall(r'>Figure [\d.]+', blob))
        ch['_interactive'] = len(re.findall(r'initBoard', blob))

    for i, ch in enumerate(chapters):
        prev_ch = chapters[i - 1] if i > 0 else None
        next_ch = chapters[i + 1] if i < len(chapters) - 1 else None
        folder = os.path.join(ROOT, f"chapter{ch['no']:02d}-{ch['slug']}")
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, 'course.html'), 'w', encoding='utf-8') as f:
            f.write(S.build_course_html(ch, prev_ch, next_ch,
                                        ch['_figures'], ch['_interactive']))
        with open(os.path.join(folder, 'exercises.html'), 'w', encoding='utf-8') as f:
            f.write(S.build_exercises_html(ch, prev_ch, next_ch))
        cr = build_coderunner(ch['coderunner'],
                              os.path.join(folder, 'exercises_coderunner.xml'))
        st = build_stack(ch['stack'], os.path.join(folder, 'exercises_stack.xml'))
        print(f"  ch{ch['no']:02d}  {ch['_figures']:2d} figures ({ch['_interactive']} interactive)"
              f"  {cr['questions']} programming / {cr['testcases']} tests"
              f"  {st['questions']} symbolic")

    with open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(S.build_index(chapters))
    print('\nindex.html written.')

    if all_fail:
        print(f'\n!! {len(all_fail)} SOLUTION TEST FAILURES:')
        for x in all_fail:
            print('   -', x)
        sys.exit(1)
    print('All reference solutions reproduce their expected outputs.')


if __name__ == '__main__':
    main()
