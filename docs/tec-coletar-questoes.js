// Coleta em JSON questões do TEC Concursos a partir da questão que está na tela.
//
// Baseado na parte de extração do userscript "TEC Concursos → JSON + Coleções" do Gunter,
// sem painel, coleções, localStorage, clipboard ou atalhos. Acrescenta o campo `cargo`, que o
// treino usa para descartar questões de cargos muito acima do concurso.
//
// Uso: o agente ajusta as duas constantes abaixo e roda o arquivo inteiro na página do TEC
// pela ferramenta de JavaScript do navegador. Devolve uma lista de questões.
// - Só ler a questão aberta, sem tocar em nada: QUANTAS = 1 e RESPONDER = false.
// - Coletar da página de filtro: QUANTAS = n e RESPONDER = true. Para cada questão, marca a
//   primeira alternativa e resolve (o gabarito só aparece depois de responder), extrai e passa
//   para a próxima. As respostas entram nas estatísticas do aluno no TEC.
//
// Vai para a skill `questoes` quando ela for criada.
const QUANTAS = 5;
const RESPONDER = true;

await (async () => {
  const limpar = (s) => (s || '')
    .replace(/ /g, ' ')
    .replace(/[ \t]+$/gm, '')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
  const texto = (el) => (el ? limpar(el.innerText) : '');
  const cru = (el) => (el ? (el.textContent || '').replace(/\s+/g, ' ').trim() : '');
  const primeiro = (scope, seletores) => {
    for (const s of seletores) {
      const el = scope.querySelector(s);
      if (el) return el;
    }
    return null;
  };
  const dormir = (ms) => new Promise((r) => setTimeout(r, ms));
  const esperar = async (cond, ms = 8000) => {
    const fim = Date.now() + ms;
    while (Date.now() < fim) {
      if (cond()) return true;
      await dormir(200);
    }
    return false;
  };

  // Sobe do enunciado até o bloco que também contém o cabeçalho da questão.
  function escopoDaQuestao(el) {
    while (el && el !== document.body) {
      if (el.querySelector('.questao-cabecalho-informacoes-materia')) return el;
      el = el.parentElement;
    }
    return document;
  }

  // Devolve sempre a letra: "Certo" vira "C" e "Errado" vira "E".
  function detectarGabarito(scope, alternativas) {
    const t = cru(scope.querySelector('.questao-enunciado-resolucao') || scope);
    const regexes = [
      /Gabarito:?\s*([A-J])\b/i,
      /Gabarito:?\s*(Certo|Errado)\b/i,
      /a\s+(?:alternativa\s+)?correta\s+é:?\s*([A-J])\b/i,
      /Você\s+selecionou:\s*([A-J]),\s*alternativa\s+correta/i
    ];
    for (const re of regexes) {
      const m = t.match(re);
      if (m) return m[1][0].toUpperCase();
    }
    const marcada = alternativas.find((a) => a.correta);
    return marcada ? marcada.letra : null;
  }

  function extrair(scope) {
    const input = scope.querySelector('input[id-questao]');
    let tecId = input && input.value ? input.value.trim() : '';
    if (!tecId) {
      const a = scope.querySelector('a.id-questao');
      if (a) tecId = (a.href || cru(a)).replace(/\D/g, '');
    }

    // Ex.: "#3291915 CEBRASPE (CESPE) - 2025 - Analista (FUNPRESP-EXE)/Sistemas..."
    const prova = cru(primeiro(scope, [
      '.questao-enunciado-concurso',
      'a[href*="/concursos/"]',
      '.resumo-questao.ng-binding'
    ]));
    const anoMatch = prova.match(/\b(19|20)\d{2}\b/);
    const partes = prova.replace(/^#\d+\s*/, '').split(' - ');

    let orgao = '';
    const orgaoEl = primeiro(scope, ['a[tec-tooltip="Link para o órgão"]', 'a[href*="/orgaos/"]']);
    if (orgaoEl) {
      const href = orgaoEl.getAttribute('ng-href') || orgaoEl.getAttribute('href') || '';
      orgao = href ? href.split('/').filter(Boolean).pop().toUpperCase() : cru(orgaoEl);
    }
    if (!orgao) {
      const logo = scope.querySelector('.questao-cabecalho-logotipo img');
      orgao = logo ? (logo.getAttribute('alt') || '').trim() : '';
    }

    const enunciadoEl = scope.querySelector('.questao-enunciado-texto');
    const alternativas = [...scope.querySelectorAll('.questao-enunciado-alternativas li')].map((li, i) => {
      const label = li.querySelector('.questao-enunciado-alternativa-opcao label') || li.querySelector('label');
      const m = cru(label).match(/[A-J]/i);
      return {
        letra: (m ? m[0] : 'ABCDEFGHIJ'[i]).toUpperCase(),
        texto: texto(li.querySelector('.questao-enunciado-alternativa-texto')),
        correta: /\b(correcao|correta|acerto|gabarito)\b/i.test(li.className)
      };
    });
    const certoErrado = alternativas.length === 2 &&
      alternativas.every((a) => /^(certo|errado)$/i.test(a.texto));
    const anulada = /anulad/i.test(cru(scope.querySelector('.questao-enunciado-resolucao'))) ||
      !!scope.querySelector('.questao-enunciado-resolucao.anulada, .questao-anulada');
    const imagens = [...(enunciadoEl ? enunciadoEl.querySelectorAll('img') : [])]
      .map((img) => img.src)
      .filter(Boolean);
    const pct = cru(scope).match(/(\d{1,3}(?:[.,]\d+)?)\s*%\s*(?:de\s*)?acert/i);

    return {
      tec_id: tecId || null,
      link: tecId ? `https://www.tecconcursos.com.br/questoes/${tecId}` : null,
      banca: cru(primeiro(scope, [
        '.resumo-questao[tec-tooltip="Link para a banca"]',
        'a[tec-tooltip="Link para a banca"]',
        'a[href*="/bancas/"]'
      ])) || null,
      ano: anoMatch ? parseInt(anoMatch[0], 10) : null,
      orgao: orgao || null,
      cargo: partes.length > 2 ? partes.slice(2).join(' - ') : null,
      prova: prova || null,
      materia: cru(scope.querySelector('.questao-cabecalho-informacoes-materia a')) || null,
      assunto: cru(primeiro(scope, [
        '.questao-cabecalho-informacoes-assunto-link a span',
        '.questao-cabecalho-informacoes-assunto-link a',
        '.questao-cabecalho-informacoes-assunto'
      ])).replace(/^Assunto:\s*/i, '') || null,
      formato_item: certoErrado ? 'certo_errado' : 'multipla_escolha',
      texto_associado: texto(primeiro(scope, [
        '.questao-texto-associado',
        '.questao-enunciado-texto-associado',
        '.texto-associado'
      ])) || null,
      enunciado: texto(enunciadoEl) || null,
      alternativas: Object.fromEntries(alternativas.map((a) => [a.letra, a.texto])),
      gabarito: anulada ? null : detectarGabarito(scope, alternativas),
      anulada,
      tem_imagem: imagens.length > 0,
      imagens,
      pct_acertos: pct ? parseFloat(pct[1].replace(',', '.')) : null,
      capturado_em: new Date().toISOString()
    };
  }

  const questaoNaTela = () => {
    const el = document.querySelector('.questao-enunciado-texto');
    return el ? extrair(escopoDaQuestao(el)) : null;
  };

  const coletadas = [];
  for (let i = 0; i < QUANTAS; i++) {
    let q = questaoNaTela();
    if (!q) break;
    if (RESPONDER && !q.gabarito && !q.anulada) {
      const alternativa = document.querySelector('#label-alternativa-0');
      if (alternativa) alternativa.click();
      await dormir(300);
      const resolver = document.querySelector('.botao-resolver');
      if (resolver) resolver.click();
      await esperar(() => {
        const x = questaoNaTela();
        return x && (x.gabarito || x.anulada);
      });
      q = questaoNaTela();
    }
    coletadas.push(q);

    if (i < QUANTAS - 1) {
      const proxima = document.querySelector('.questao-navegacao-botao-proxima.ng-isolate-scope');
      if (!proxima) break;
      proxima.click();
      const mudou = await esperar(() => {
        const x = questaoNaTela();
        return x && x.tec_id && x.tec_id !== q.tec_id;
      });
      if (!mudou) break;
    }
  }
  return coletadas;
})();
