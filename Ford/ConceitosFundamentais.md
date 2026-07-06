# 📘 Conceitos Fundamentais — Teste Automotivo Embarcado

Material de apoio para a seção **3.1 Fundamentos de Teste Automotivo Embarcado** do repositório de estudos.

---

## 1. V-Model (Modelo em V)

O V-Model é o modelo de desenvolvimento mais usado na indústria automotiva. Ele organiza o ciclo de vida do software/sistema em dois braços que se espelham:

```
Requisitos do Sistema  ──────────────────────────  Teste de Sistema
      \                                                    /
   Requisitos de                                    Teste de
   Software (SRS)                                 Integração
        \                                              /
     Arquitetura                                   Teste de
     (Design)                                    Componente/Unidade
          \                                          /
              Implementação (Código)
```

- **Lado esquerdo (descendo):** cada etapa de especificação/design gera um artefato mais detalhado (do requisito geral do veículo até o código de uma função específica).
- **Lado direito (subindo):** cada nível de teste **valida** o artefato correspondente criado do lado esquerdo. Ou seja, teste de unidade valida o código, teste de integração valida a arquitetura, teste de sistema valida os requisitos de software, e assim por diante.
- **Por que importa para o projeto:** o "AutoTest Framework" atua justamente nesses níveis de verificação — ele precisa saber identificar em qual "V" um script pertence, porque a estratégia de correção muda dependendo do nível (um script de teste de unidade quebra por outro motivo que um script de teste de sistema).

---

## 2. MIL / SIL / HIL

Esses três termos descrevem **em que ambiente o software está rodando durante o teste** — é basicamente uma escada de "quão perto do hardware real" o teste está sendo executado.

### MIL — Model-in-the-Loop

- O algoritmo/função ainda está em forma de **modelo** (ex: Simulink/MATLAB), antes de virar código C/C++ final.
- Serve para validar a **lógica de controle** (ex: um algoritmo de controle de temperatura do ar-condicionado) antes de gerar código.
- Nenhum hardware real está envolvido; tudo roda em simulação no PC.

### SIL — Software-in-the-Loop

- O modelo já foi convertido em **código-fonte real** (ou o código de produção em si), mas ainda roda em um PC comum, **sem** o microcontrolador/ECU real.
- Permite testar a lógica do software já "próxima da produção", com execução rápida e barata (sem precisar de bancada física).
- Muito usado para rodar **suítes grandes de testes automatizados** rapidamente, já que não depende de hardware físico disponível.

### HIL — Hardware-in-the-Loop

- O software de produção roda **dentro do hardware real** (a ECU física), mas o "mundo ao redor" dela (motor, sensores, outros módulos do carro) é **simulado** por uma bancada especializada.
- É o nível mais próximo da realidade sem precisar do veículo inteiro.
- Mais caro e mais lento para rodar do que SIL, mas pega problemas que só aparecem com o hardware real (timing, interrupções, drivers).

**Resumo da progressão:**

```
MIL (modelo)  →  SIL (código em PC)  →  HIL (código em hardware real, ambiente simulado)  →  Veículo real
```

Quanto mais à direita, mais realista e mais caro/lento. Times de automação tentam rodar o máximo de testes possível em SIL, deixando HIL para os casos que realmente precisam do hardware.

---

## 3. Níveis de Teste no Contexto Veicular

| Nível | O que valida | Exemplo no Radio App |
|---|---|---|
| **Unidade** | Uma função/método isolado | Testar a função que formata o nome da estação de rádio |
| **Integração** | Comunicação entre módulos/componentes | Testar se o módulo de Bluetooth consegue passar dados pro módulo de áudio |
| **Sistema** | O sistema completo, comportando-se como um todo | Ligar o carro, trocar de estação de rádio, verificar se o som sai corretamente |
| **Aceitação** | Se o sistema atende ao que o cliente/negócio espera | Validar com critérios definidos pela Ford se a experiência do usuário está de acordo com o esperado |

Isso conecta direto com o V-Model: cada um desses níveis é uma "perna direita" correspondente a uma etapa de especificação da "perna esquerda".

---

## 4. Infotainment e Arquitetura de ECUs

- **ECU (Electronic Control Unit):** um computador dedicado dentro do carro, responsável por controlar um subsistema específico (motor, freios, airbag, infotainment, etc). Um carro moderno pode ter dezenas de ECUs.
- **Head Unit:** é a ECU específica que roda o sistema de **infotainment** — a tela central, rádio, navegação, conectividade com celular (Android Auto/CarPlay), etc. É essa ECU que hospeda o "Radio App" citado no projeto.
- **IVI (In-Vehicle Infotainment):** o termo genérico da indústria para esse tipo de sistema (head unit + software + apps rodando nele).
- Muitas head units modernas rodam em cima de **Android Automotive** ou sistemas Linux customizados, o que significa que ferramentas de automação de UI (como Appium) fazem sentido nesse contexto.

---

## 5. Protocolos de Comunicação Veicular

### CAN (Controller Area Network)

- Protocolo de rede **mais usado** dentro dos veículos para comunicação entre ECUs.
- Baseado em **mensagens com prioridade** (arbitração por ID) transmitidas em um barramento compartilhado — todas as ECUs "ouvem" tudo e filtram o que interessa.
- Velocidade típica: até 1 Mbps (CAN clássico).
- É o motivo pelo qual a biblioteca **python-can** é relevante para o projeto — ela permite enviar/ler mensagens CAN via script Python.

### CAN-FD (CAN with Flexible Data-Rate)

- Evolução do CAN clássico: permite **payloads maiores** (até 64 bytes, contra 8 bytes do CAN clássico) e **velocidades maiores** na fase de dados.
- Criado porque sistemas modernos (como infotainment) trocam mais dados do que o CAN clássico suporta confortavelmente.

### LIN (Local Interconnect Network)

- Protocolo **mais simples e barato** que o CAN, usado para componentes menos críticos (ex: controle de vidro elétrico, espelhos, bancos elétricos).
- Um "mestre" controla vários "escravos" — não tem a mesma robustez/prioridade do CAN.

### Ethernet Automotivo

- Tecnologia mais recente, usada quando é preciso **muita largura de banda** — por exemplo, câmeras de assistência ao motorista, sensores de ADAS, ou grandes volumes de dados de infotainment (streaming, atualizações OTA).
- Permite velocidades de 100 Mbps a vários Gbps, muito acima do CAN/CAN-FD.

**Por que isso importa para o projeto:** o Radio App provavelmente se comunica com outras ECUs via CAN (ex: para saber status do veículo) e possivelmente Ethernet (para dados mais pesados). Entender esses protocolos ajuda a entender **por que** um script de teste pode quebrar — às vezes não é o app que mudou, é a mensagem CAN que ele espera receber que mudou de formato.

---

## 6. Normas Relevantes

### ASPICE (Automotive SPICE)

- Um **modelo de maturidade de processo** (não é uma norma de produto) usado pela indústria automotiva para avaliar o quão bem uma empresa/fornecedor segue processos de engenharia de software.
- Define níveis (0 a 5) de capacidade em processos como gestão de requisitos, teste, gestão de configuração, etc.
- Relevante para o projeto porque frameworks de automação de teste em ambiente automotivo geralmente precisam gerar **evidências rastreáveis** (traceability) entre requisito → teste → resultado, para atender às exigências ASPICE dos processos da montadora/fornecedores.

### ISO 26262

- Norma de **segurança funcional** para sistemas elétricos/eletrônicos automotivos.
- Define os famosos **ASIL** (Automotive Safety Integrity Level — de QM até ASIL D, sendo D o mais crítico).
- Como o Radio App (infotainment) geralmente **não é um sistema de safety crítico** (diferente de freios, airbag, direção), essa norma tende a ter menor peso no projeto — mas é bom saber que ela existe e por que outros sistemas do carro são tratados com mais rigor.

---

## 7. Como Tudo se Conecta ao Projeto AutoTest Framework

| Conceito | Onde entra no projeto |
|---|---|
| V-Model | Ajuda a categorizar em que nível cada script de teste quebrado está |
| SIL | Provavelmente o ambiente onde a maioria dos testes automatizados do framework roda (mais rápido/barato que HIL) |
| HIL | Pode ser necessário para validar cenários que dependem do hardware real da head unit |
| CAN/CAN-FD | Scripts de teste podem enviar/receber mensagens CAN simuladas para testar o Radio App |
| ASPICE | Exige rastreabilidade — o framework provavelmente precisa gerar relatórios ligando requisito → teste → resultado |
| ISO 26262 | Provavelmente baixo impacto direto, já que infotainment não é tipicamente safety-critical |

---

## 8. Glossário Expandido

| Termo | Significado |
|---|---|
| HIL | Hardware-in-the-Loop — teste com hardware real e ambiente simulado |
| SIL | Software-in-the-Loop — teste do código real rodando em PC, sem hardware |
| MIL | Model-in-the-Loop — teste do modelo (Simulink/MATLAB) antes de virar código |
| CI/CD | Integração Contínua / Entrega Contínua |
| ECU | Electronic Control Unit — computador dedicado a um subsistema do carro |
| IVI | In-Vehicle Infotainment — sistema de infotainment embarcado |
| Head Unit | A ECU física que roda o sistema de infotainment |
| ASPICE | Automotive SPICE — modelo de maturidade de processo de engenharia |
| ASIL | Automotive Safety Integrity Level — nível de criticidade de segurança (ISO 26262) |
| CAN | Controller Area Network — protocolo de rede veicular por mensagens priorizadas |
| CAN-FD | CAN com taxa de dados flexível — payloads maiores e mais velocidade |
| LIN | Local Interconnect Network — protocolo simples mestre-escravo para componentes não críticos |
| Flaky test | Teste que falha/passa de forma inconsistente sem mudança real no código |
| Rastreabilidade (traceability) | Capacidade de ligar um requisito a seus testes e resultados correspondentes |
