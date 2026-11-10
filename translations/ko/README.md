<p align="center">
  <img src="../../assets/readme/header.png" alt="ship-beautiful-ui: one skill from prompt to polished UI. No more AI-looking UI." width="840">
</p>

<p align="center">
  <b>코딩 에이전트를 프롬프트에서 완성도 높은 UI까지 이끄는 하나의 skill.<br>자체 디자인 라이브러리, 자체 검사, 그리고 템플릿이 아닌 여러분의 주제에서 나오는 디자인.</b>
</p>

```bash
npx skills add Vedmeena21/ship-beautiful-ui
```

<p align="center">
  <a href="../../LICENSE"><img src="https://img.shields.io/badge/license-MIT-0F1115?style=flat-square" alt="MIT License"></a>
  <a href="../../skills/ship-beautiful-ui/SKILL.md"><img src="https://img.shields.io/badge/Agent%20Skill-SKILL.md-2B59FF?style=flat-square" alt="Agent Skill"></a>
  <img src="https://img.shields.io/badge/works%20with-Claude%20Code%20%C2%B7%20Codex%20%C2%B7%20Cursor-2B59FF?style=flat-square" alt="Works with Claude Code, Codex and Cursor">
  <img src="https://img.shields.io/badge/dependencies-none-0F1115?style=flat-square" alt="No dependencies">
  <a href="https://github.com/Vedmeena21/ship-beautiful-ui/stargazers"><img src="https://img.shields.io/github/stars/Vedmeena21/ship-beautiful-ui?style=flat-square&color=2B59FF" alt="GitHub stars"></a>
  <a href="../../translations"><img src="https://img.shields.io/badge/languages-13-2B59FF?style=flat-square" alt="README in 13 languages"></a>
</p>

<p align="center">
  <a href="#설치">설치</a> ·
  <a href="#작동-방식">작동 방식</a> ·
  <a href="#여러분의-브랜드-여러분의-색">여러분의 브랜드, 여러분의 색</a> ·
  <a href="#구성">구성</a>
</p>

| 흔한 AI 첫 초안 | ship-beautiful-ui로 만든 결과 |
|:---:|:---:|
| <img src="../../assets/readme/before.jpg" alt="Proofsheet, an invoicing tool for photographers, styled the default AI way: dark page, centered purple-to-blue gradient headline, emoji chips and a glowing glass card" width="420"> | <img src="../../assets/readme/after.jpg" alt="The same page and words redesigned with ship-beautiful-ui: a paper-white page with a serif headline 'Invoice the shoot before you finish the edit' and the real product: the invoice on a phone, ready to send" width="420"> |

<details>
<summary>🌐 다국어 지원</summary>

[English](../../README.md) | [Arabic](../ar/README.md) | [Chinese (Simplified)](../zh/README.md) | [French](../fr/README.md) | [German](../de/README.md) | [Hindi](../hi/README.md) | [Indonesian](../id/README.md) | [Japanese](../ja/README.md) | [Korean](../ko/README.md) | [Portuguese (Brazil)](../pt-BR/README.md) | [Russian](../ru/README.md) | [Spanish](../es/README.md) | [Turkish](../tr/README.md)

</details>

---

## 왜 만들었나

코딩 에이전트는 몇 분 만에 프론트엔드 전체를 작성하지만, 결과물은 여전히 다른 AI 페이지와 똑같아 보입니다. 같은 폰트, 같은 보라색 그라디언트, 똑같은 카드 세 개가 나란히 있는 줄, 모든 섹션에 같은 페이드업.

에이전트가 매번 같은 기본값에서 시작하기 때문입니다. **ship-beautiful-ui**는 그 기본값을 프로세스, 실제 디자인 데이터, 그리고 결과물에 실행되는 검사로 바꿉니다:

- **프로세스.** 브리프 → 방향 → 고정 → 빌드 → 모션 → 리뷰, 항상 이 순서로.
- **주제에서 출발하는 디자인.** 팔레트는 모두가 쓰는 목록이 아니라 제품 고유의 세계(빵집의 빵 껍질과 밀가루, 암실 안전등의 빨강)에서 나옵니다.
- **하나의 기준 문서.** 모든 시각적 결정은 코드보다 먼저 `DESIGN.md`에 기록되고 검사됩니다.
- **느낌이 아닌 검사.** 40개 규칙의 탐지기가 전달 전에 코드에서 AI 티와 접근성 문제를 찾아냅니다.

의존성 없음. 스크립트는 순수 Python 3입니다.

## 설치

**모든 에이전트 (Claude Code, Codex, Cursor 등)** [`skills`](https://github.com/vercel-labs/skills) CLI로:

```bash
npx skills add Vedmeena21/ship-beautiful-ui
```

**Claude Code 플러그인:**

```
/plugin marketplace add Vedmeena21/ship-beautiful-ui
/plugin install ship-beautiful-ui@ship-beautiful-ui
```

**수동:** [`skills/ship-beautiful-ui`](../../skills/ship-beautiful-ui)를 `.claude/skills/`(프로젝트) 또는 `~/.claude/skills/`(전역)에 복사하세요.

**그다음엔 UI를 요청하기만 하면 됩니다.** 페이지, 화면, 컴포넌트를 만들거나 다시 디자인하거나 다듬을 때 skill이 알아서 시작됩니다:

```
프리랜서 사진작가를 위한 청구서 도구의 랜딩 페이지를 만들어 줘.
목표는 하나: 첫 청구서를 2분 안에 보내기. Next.js + Tailwind.
```

```
이 대시보드는 너무 평범해 보여. ship-beautiful-ui로 다시 디자인해 줘.
```

세 가지를 돌려받습니다:

| 결과물 | 내용 |
|---|---|
| `DESIGN.md` | 여러분의 디자인 시스템: 어떤 에이전트든 읽을 수 있는 토큰과 규칙, 대비 검사 완료 |
| UI | `DESIGN.md` 토큰만으로 구축 |
| `REVIEW.md` | 탐지기가 찾은 것, 고친 것, 유지한 것과 그 이유 |

## 작동 방식

<p align="center">
  <img src="../../assets/readme/pipeline.svg" alt="The six-step pipeline: brief, direction, lock in DESIGN.md, build, motion, review" width="840">
</p>

| 단계 | 하는 일 | 내장 |
|---|---|---|
| **0. 브리프** | 주제, 대상, 화면의 단 하나의 목적, 주제의 세계에서 나온 명사 다섯 개 | [`00-brief.md`](../../skills/ship-beautiful-ui/references/00-brief.md) |
| **1. 방향** | 이 주제를 위한 팔레트, 서체 조합, 레이아웃 | `derive.py`, `direction.py`, 78개 소재, 60개 팔레트, 40개 서체 조합, 20개 레이아웃 |
| **2. 고정** | 모든 결정을 `DESIGN.md`에 기록하고 검사 | `lint_design.py`, [`DESIGN.md` 템플릿](../../skills/ship-beautiful-ui/templates/DESIGN.md) |
| **3. 빌드** | 토큰만, 대담한 아이디어 하나, 품질 하한선 | [`effects.md`](../../skills/ship-beautiful-ui/references/effects.md) (16개 효과), [`ux-rules.md`](../../skills/ship-beautiful-ui/references/ux-rules.md) (80개 규칙) |
| **4. 모션** | 변화를 설명하는 모션만 | [`04-motion.md`](../../skills/ship-beautiful-ui/references/04-motion.md): 타이밍 토큰과 12개 레시피 |
| **5. 리뷰** | 전달 전 하나의 관문 | `detect.py` (40개 규칙), 스크린샷, [`REVIEW.md`](../../skills/ship-beautiful-ui/templates/REVIEW.md) |

**지시가 충돌할 때 우선순위:** 여러분의 말 > `DESIGN.md` > skill의 규칙 > 그 밖에 불러온 모든 것. 에이전트는 충돌을 해결할 때 이를 분명히 말하므로 여러분이 뒤집을 수 있습니다.

## 여러분의 브랜드, 여러분의 색

에이전트에게 제품이 무엇인지 알려 주면, 모두가 쓰는 목록이 아니라 그 제품을 위해 디자인합니다. 브랜드 색이 있는 회사에서 일한다면 그 색을 씁니다. 아직 브랜드가 없다면 어울리는 색을 고릅니다.

- **브랜드가 있다면.** 색을 알려 주면 그대로 유지됩니다. 에이전트가 실제 UI에 필요한 나머지(텍스트, 테두리, 호버와 오류 색)를 채워 줍니다.
- **아직 없다면.** 제품을 몇 단어로 설명하면 에이전트가 제품에 어울리는 색을 고릅니다.
- **아직 잘 모르겠다면?** `direction.py`가 고를 수 있는 세 가지 완성된 스타일을 제안합니다.

어느 쪽이든, 코드 한 줄을 쓰기 전에 모든 색이 읽기 쉬운지(WCAG AA) 검사합니다.

## 구성

에이전트가 프로처럼 디자인하는 데 필요한 모든 것이 하나의 폴더에. 계정도, API 키도, 추가 설치도 필요 없습니다.

| 제공되는 것 | 개수 | 왜 중요한가 |
|---|:---:|---|
| 실제 세계의 소재 | **78** | 크라프트지, 에스프레소, 이끼, 필름 같은 것에서 가져온 색으로 팔레트가 제품에 어울립니다 |
| 컬러 팔레트 | **60** | 바로 쓸 수 있는 라이트와 다크, 모두 가독성 테스트 완료 |
| 폰트 조합 | **40** | 잘 어울리는 제목용과 본문용 폰트, 모두 무료 Google Fonts |
| 페이지 레이아웃 | **20** | 스케치가 포함된 검증된 페이지 구조: 제품 히어로, 에디토리얼, 대시보드, 요금제 등 |
| 시각 효과 | **16** | 그레인, 글로우, 스포트라이트, 마키, 틸트 등: 여러분의 색을 쓰고 동작 줄이기 설정을 존중하는 복사·붙여넣기 CSS |
| 애니메이션 레시피 | **12** | 버튼, 메뉴, 모달, 토스트, 탭, 목록이 모두 같은 세련된 방식으로 움직입니다 |
| UX 규칙 | **80** | 폼, 내비게이션, 표, 차트, 모바일, 빈 상태와 오류 상태를 위한 체크리스트 |
| 탐지기 검사 | **40** | 배포 전에 AI 티와 접근성 문제를 잡아냅니다 |

## 라이선스

[MIT](../../LICENSE). **Ved Prakash Meena**가 만들고 관리합니다.

<a href="https://www.linkedin.com/in/ved-prakash-meena"><img src="https://img.shields.io/badge/Follow%20on%20LinkedIn-Ved%20Prakash%20Meena-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="Follow Ved Prakash Meena on LinkedIn"></a>

<p align="center">
  <sub>"AI 느낌 좀 덜 나게 해 줘"를 한 번이라도 줄였다면 ⭐ 하나가 다른 사람들이 찾는 데 도움이 됩니다. 더 많은 소식은 <a href="https://www.linkedin.com/in/ved-prakash-meena">LinkedIn에서 팔로우</a>하세요.</sub>
</p>
