const fs=require('fs'), vm=require('vm'), path=require('path');
// Node-only grammar check: there is no HTML DOM; sanitizer is an identity stub.
// Mermaid grammar/parser code is unchanged. This does not render SVG or test HTML sanitization.
let library=fs.readFileSync('/tmp/tamarix-mermaid.min.js','utf8').replaceAll('fl.sanitize(', 'String(').replaceAll('fl.addHook(', '(()=>{})(');
const box={console,setTimeout,clearTimeout,structuredClone};
vm.createContext(box);vm.runInContext(library,box);
box.mermaid.initialize({startOnLoad:false,securityLevel:'loose',flowchart:{htmlLabels:false}});
(async()=>{
 const results=[];
 for(const file of fs.readdirSync('docs').filter(f=>f.endsWith('.md')).sort()){
  let index=0;
  for(const match of fs.readFileSync(path.join('docs',file),'utf8').matchAll(/```mermaid\n([\s\S]*?)\n```/g)){
   const id=file+':'+(++index);
   try{const result=await box.mermaid.parse(match[1]);results.push({id,status:'PASS',diagramType:result.diagramType});}
   catch(e){results.push({id,status:'FAIL',error:e.message});}
  }
 }
 fs.writeFileSync('/tmp/tamarix-mermaid-parser-results.json',JSON.stringify({status:results.every(r=>r.status==='PASS')?'PASS':'FAIL',source:'Installed Obsidian Mermaid bundle; HTML sanitizer stub for Node-only grammar validation',results},null,2));
 console.log(JSON.stringify(results,null,2));process.exitCode=results.some(r=>r.status==='FAIL')?1:0;
})();
