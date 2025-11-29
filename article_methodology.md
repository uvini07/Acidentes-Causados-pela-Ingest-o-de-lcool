# Metodologia e Processo de Construção do Artigo

Durante o desenvolvimento deste trabalho, procurei seguir uma metodologia organizada para garantir que todas as etapas, desde a coleta dos dados até a elaboração dos gráficos e da análise final, fossem realizadas de forma lógica e fundamentada. A seguir descrevo, passo a passo, como construí o artigo e quais foram meus pensamentos durante o processo.

---

## 1. Definição do tema e da hipótese

O primeiro passo foi definir exatamente qual questão eu queria investigar. A partir de estudos iniciais e observando a realidade do trânsito, percebi que muitos acidentes acontecem nos finais de semana, possivelmente relacionados ao consumo de álcool e ao cansaço.

Com isso, formulei a hipótese central do trabalho:

> **Acidentes causados por álcool e fadiga tendem a ser mais frequentes aos sábados e domingos.**

Essa hipótese orientou todas as etapas seguintes.

---

## 2. Coleta dos dados

Decidido o tema, comecei a buscar bases públicas com registros de acidentes de trânsito. Optei por usar bancos de dados oficiais porque eles já contêm informações estruturadas, como data, horário e causa do acidente.

Meu objetivo, desde o começo, era garantir que as análises fossem baseadas em evidências reais, e não apenas em percepções gerais.

---

## 3. Limpeza e organização dos dados

Assim que importei os dados para o ambiente de desenvolvimento, iniciei um processo de limpeza. Nesta etapa, fiz:

- padronização de datas e horários;  
- exclusão de registros incompletos;  
- reorganização das colunas;  
- criação de uma categoria específica chamada **“Álcool e fadiga”**, que agrupava os motivos relacionados.

Percebi que, sem essa reorganização, seria difícil gerar comparações consistentes entre os dias da semana.

---

## 4. Separação entre finais de semana e dias úteis

Após deixar o banco de dados limpo, categorizei os dias em dois grupos:

- **Segunda a sexta → Dias úteis**  
- **Sábado e domingo → Finais de semana**

Essa etapa foi essencial para começar a testar se a minha hipótese realmente fazia sentido.

---

## 5. Construção da análise exploratória

Com os dados prontos, iniciei a análise exploratória usando Python. Meu objetivo aqui foi observar padrões gerais antes de fazer testes estatísticos.

As principais bibliotecas utilizadas foram:

- **pandas** para manipulação dos dados;  
- **numpy** para cálculos simples;  
- **matplotlib** e **seaborn** para geração de gráficos.

Durante essa fase, criei tabelas de frequência e gráficos que mostravam como os acidentes se distribuíam ao longo da semana. Foi aqui que comecei a perceber visualmente que os finais de semana realmente tinham picos.

---

## 6. Geração dos gráficos

Para facilitar a interpretação e enriquecer o artigo, produzi diversos tipos de gráficos:

- gráficos de barras comparando dias da semana e finais de semana;  
- gráficos de linha mostrando a distribuição ao longo da semana;  
- **heatmap** para destacar horários críticos;  
- histogramas e gráficos de densidade para analisar concentração de ocorrências.

Enquanto criava os gráficos, busquei manter um padrão de cores e estilos para deixar os resultados mais agradáveis visualmente e fáceis de entender.

---

## 7. Testes estatísticos (Qui-Quadrado)

Depois de visualizar os padrões iniciais, realizei o **teste Qui-Quadrado** para confirmar se as diferenças observadas entre dias úteis e finais de semana eram estatisticamente significativas.

Ao perceber que o **valor de p era menor que 0,05**, concluí que a diferença realmente não ocorreu por acaso, reforçando a hipótese inicial.

Essa etapa foi importante porque deu validade científica à análise.

---

## 8. Interpretação dos resultados

Com os gráficos e o teste estatístico concluídos, passei para a interpretação. Observei que:

- acidentes relacionados a álcool e fadiga aumentam nos finais de semana;  
- os horários mais críticos são as noites de sábado e madrugadas de domingo;  
- os padrões se alinham com estudos anteriores encontrados na literatura.

A interpretação foi escrita sempre buscando conciliar meus achados com referências teóricas.

---

## 9. Integração da transformação digital no contexto do estudo

Como parte da proposta, também analisei como ferramentas digitais e ciência de dados contribuem para a segurança viária.

Durante a redação, procurei conectar minha experiência prática com o uso de Python e visualização de dados à ideia de transformação digital, mostrando que:

- tecnologias ajudam na análise preditiva;  
- painéis digitais podem orientar políticas públicas;  
- monitoramento inteligente reduz riscos.

Essa reflexão complementou a análise e tornou o artigo mais atual.

---

## 10. Redação final

Na última etapa, revisei todo o conteúdo produzido e organizei o texto do artigo com mais clareza. Nesse processo, contei com a orientação da professora do Senai Suíço-Brasileira, doutora em Matemática Computacional e engenheira de dados, que me ajudou a entender a melhor forma de apresentar os resultados e fortalecer a coerência entre as análises e as conclusões. Com o apoio dela, refinei a escrita, ajustei os gráficos e garanti que o trabalho ficasse bem estruturado e fiel aos dados estudados.

---
