# 📌 Bolsa INOVA IEL — Ford Motor Company Brasil

## Projeto: AutoTest Framework — Plataforma de Correção de Scripts de Teste Automatizados para Sistemas Veiculares

---

## 1. Contexto do Projeto

- **Outorgante:** Instituto Euvaldo Lodi (IEL/BA)
- **Empresa:** Ford Motor Company Brasil Ltda
- **Tutor:** Adriano Santana Almeida da Silva (<asilv562@ford.com>)
- **Programa:** Bolsa INOVA IEL (pesquisa científica, desenvolvimento tecnológico e inovação)

### Objetivo do projeto

Desenvolver uma **plataforma de correção de scripts de teste automatizados**, capaz de:

- Identificar scripts **não funcionais** quando surgem novas versões de software (do **Radio App** / infotainment).
- Permitir **versionamento** desses scripts e sua **correção automática ou assistida**.
- Reduzir o esforço manual de verificação de testes.
- Aumentar **cobertura** e **confiabilidade** dos testes.
- Integrar-se aos **pipelines de CI/CD** existentes.

### Fases do projeto (linha do tempo)

1. Ford Setup (ambientação, acessos, ferramentas internas)
2. Análise de Requisitos e Desenho da Arquitetura
3. Desenvolvimento Iterativo do Framework e dos Testes
4. Integração com CI/CD e Execução do Projeto Piloto
5. Testes e Ajustes
6. Documentação, Treinamento e Relatório Final

### Por que isso importa (relevância de negócio)

- **Qualidade/confiabilidade:** detectar bugs cedo evita recalls e dano de reputação.
- **Time-to-market:** testes automatizados aceleram entregas (alinhado a Agile/DevOps).
- **Redução de custo operacional:** menos trabalho manual repetitivo.
- **Escalabilidade:** veículos cada vez mais "software-defined" exigem automação robusta.

---

## 2. O que é o "Radio App"?

É o sistema de infotainment do veículo (rádio, tela central, conectividade, apps).
Ele roda testes automatizados que, a cada nova versão de software, podem **quebrar** (scripts ficam desatualizados/obsoletos). O projeto quer criar uma ferramenta que:

- Roda a suíte de testes.
- Detecta quais scripts falharam por causa de **mudança legítima** no sistema (não é bug, é o script que ficou desatualizado).
- Sugere ou aplica a correção.
- Versiona o histórico dessas correções.

---

## 3. Trilha de Estudos

### 3.1 Fundamentos de Teste Automotivo Embarcado

- [ ] **V-Model** de desenvolvimento automotivo (onde entra cada tipo de teste)
- [ ] **MIL** (Model-in-the-Loop)
- [ ] **SIL** (Software-in-the-Loop)
- [ ] **HIL** (Hardware-in-the-Loop)
- [ ] Diferença entre teste de **unidade**, **integração**, **sistema** e **aceitação** no contexto veicular
- [ ] O que é **infotainment** / arquitetura de ECUs relacionadas (head unit, IVI)
- [ ] Protocolos de comunicação veicular: **CAN**, **CAN-FD**, **LIN**, **Ethernet automotivo**
- [ ] Normas relevantes: **ASPICE**, **ISO 26262** (visão geral, não precisa aprofundar se não for função safety)

### 3.2 Python para Testes Automatizados

- [ ] **Pytest** (fixtures, parametrize, marks, plugins, relatórios)
- [ ] **unittest** (caso a empresa use como legado)
- [ ] **pyserial** (comunicação serial com hardware/bancada)
- [ ] **python-can** (envio/leitura de mensagens CAN)
- [ ] **Robot Framework** (testes orientados a keyword, muito comum em times automotivos)
- [ ] **Appium** (automação de UI para telas de infotainment / Android Automotive)
- [ ] Manipulação de logs e parsing (regex, `re`, `logging`)
- [ ] Estrutura de projeto de automação (Page Object / Screen Object pattern adaptado a HMI)

### 3.3 Versionamento e Detecção de Scripts Quebrados

- [ ] **Git** (branching, tags, versionamento semântico — útil pro "versionamento" citado no projeto)
- [ ] Estratégias de **diffing** entre versões de scripts de teste
- [ ] Técnicas de **auto-healing tests** (self-healing test automation) — muito relevante para "correção automática de scripts"
- [ ] Detecção de **flaky tests**
- [ ] Análise estática de código Python (`ast`, `flake8`, `pylint`) — pode ser usada para identificar scripts quebrados estruturalmente

### 3.4 CI/CD

- [ ] Conceitos gerais de **CI/CD** (pipelines, stages, artifacts)
- [ ] Ferramentas comuns: **Jenkins**, **GitLab CI**, **GitHub Actions**, **Azure DevOps**
- [ ] Como plugar suítes Pytest/Robot Framework em um pipeline
- [ ] Geração de relatórios de teste (JUnit XML, Allure, HTML reports)
- [ ] Execução de testes em paralelo / distribuídos (ex: `pytest-xdist`)

### 3.5 Arquitetura de Software (para "Desenho da Arquitetura")

- [ ] Arquitetura em camadas (já familiar pelo SendYouAI — reaproveitar conceito)
- [ ] Design de uma ferramenta de "correção de scripts" — pensar em:
  - Módulo de execução de testes
  - Módulo de análise/diagnóstico de falhas
  - Módulo de sugestão/aplicação de correção
  - Módulo de versionamento/histórico
- [ ] Bancos de dados para armazenar histórico de execuções (SQL Server/PostgreSQL — já tem experiência)

### 3.6 Soft Skills / Entregáveis do Projeto

- [ ] Como escrever um **Plano de Trabalho** técnico
- [ ] Como estruturar um **Relatório Final** de projeto de inovação
- [ ] Preparar material de **Treinamento** (documentação para outros usarem o framework)

---

## 4. Ideias de Estudo Prático (hands-on)

- [ ] Montar um mini projeto Pytest que simula "scripts de teste" e detecta quando um deles quebra por mudança de versão de um "software fake"
- [ ] Testar `python-can` com um bus virtual (`virtualcan`/`socketcan` no Linux) para simular mensagens CAN
- [ ] Criar um pipeline simples no GitHub Actions rodando Pytest + gerando relatório
- [ ] Explorar Robot Framework com uma suíte de exemplo e comparar com Pytest

---

## 5. Referências para Buscar

- Documentação oficial: Pytest, Robot Framework, python-can, pyserial, Appium
- Artigos sobre "self-healing test automation"
- ASPICE overview (visão de processo, não certificação completa)
- Android Automotive / infotainment testing (se o Radio App for baseado em Android)

---

## 6. Glossário Rápido

| Termo | Significado |

|---|---|
| HIL | Hardware-in-the-Loop |
| SIL | Software-in-the-Loop |
| MIL | Model-in-the-Loop |
| CI/CD | Integração Contínua / Entrega Contínua |
| ECU | Electronic Control Unit |
| IVI | In-Vehicle Infotainment |
| ASPICE | Automotive SPICE (modelo de maturidade de processo) |
| Flaky test | Teste que falha/passa de forma inconsistente sem mudança no código |
