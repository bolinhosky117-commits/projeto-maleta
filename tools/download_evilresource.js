// Baixa a imagem grande ("full") de todos os itens de uma página de listagem do Evil Resource
// e salva tudo num único .zip (sem compressão), direto pelo navegador.
//
// Como usar:
// 1. Abra no navegador a página de listagem, ex.:
//      https://www.evilresource.com/resident-evil-4-remake/weaponry
//      https://www.evilresource.com/resident-evil-4-remake/items
// 2. Abra o console (F12 > Console), cole este arquivo inteiro e aperte Enter.
// 3. Para pegar só uma seção (ex.: "Recovery items"), mude SECTION abaixo para o texto do título.
//    Deixe null para pegar todos os itens da página.

(async () => {
  const SECTION = null;            // ex.: "Recovery items"
  const ZIP_NAME = "evilresource-images.zip";

  const sectionPath = location.pathname.replace(/\/$/, "");
  let anchors;
  if (SECTION) {
    const h = [...document.querySelectorAll("h2,h3")].find(x => x.textContent.trim().toLowerCase().includes(SECTION.toLowerCase()));
    if (!h) throw new Error("Seção não encontrada: " + SECTION);
    anchors = [];
    let n = h.nextElementSibling;
    while (n && !/^H[23]$/.test(n.tagName)) { anchors.push(...n.querySelectorAll(`a[href*="${sectionPath}/"]`)); n = n.nextElementSibling; }
  } else {
    anchors = [...document.querySelectorAll(`a[href*="${sectionPath}/"]`)];
  }
  const links = [...new Set(anchors.map(a => a.href).filter(h => !h.includes("#")))];
  console.log(links.length, "itens");

  const files = [], fails = [];
  for (const u of links) {
    try {
      const d = new DOMParser().parseFromString(await fetch(u).then(r => r.text()), "text/html");
      const img = d.querySelector('img[src*="/images/data/full/"]');
      if (!img) { fails.push(u); continue; }
      const src = new URL(img.getAttribute("src"), location.origin).href;
      const slug = u.split("/").pop();                 // nome do arquivo = slug da página (evita duplicados)
      const ext = src.split("?")[0].split(".").pop();
      files.push({ name: `${slug}.${ext}`, buf: new Uint8Array(await fetch(src).then(r => r.arrayBuffer())) });
    } catch (e) { fails.push(u + " " + e); }
  }

  // ZIP "store" mínimo
  const T = new Uint32Array(256);
  for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; T[n] = c >>> 0; }
  const crc = b => { let c = 0xFFFFFFFF; for (let i = 0; i < b.length; i++) c = T[(c ^ b[i]) & 255] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; };
  const enc = new TextEncoder(), parts = [], central = []; let off = 0;
  for (const f of files) {
    const nb = enc.encode(f.name), c = crc(f.buf);
    const h = new DataView(new ArrayBuffer(30));
    h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint32(14, c, true);
    h.setUint32(18, f.buf.length, true); h.setUint32(22, f.buf.length, true); h.setUint16(26, nb.length, true);
    parts.push(h.buffer, nb, f.buf);
    const cd = new DataView(new ArrayBuffer(46));
    cd.setUint32(0, 0x02014b50, true); cd.setUint16(4, 20, true); cd.setUint16(6, 20, true); cd.setUint32(16, c, true);
    cd.setUint32(20, f.buf.length, true); cd.setUint32(24, f.buf.length, true); cd.setUint16(28, nb.length, true); cd.setUint32(42, off, true);
    central.push(cd.buffer, nb);
    off += 30 + nb.length + f.buf.length;
  }
  const cdSize = central.reduce((s, p) => s + (p.byteLength ?? p.length), 0);
  const e = new DataView(new ArrayBuffer(22));
  e.setUint32(0, 0x06054b50, true); e.setUint16(8, files.length, true); e.setUint16(10, files.length, true);
  e.setUint32(12, cdSize, true); e.setUint32(16, off, true);
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([...parts, ...central, e.buffer], { type: "application/zip" }));
  a.download = ZIP_NAME; document.body.appendChild(a); a.click();
  console.log("OK:", files.length, "falhas:", fails);
})();
