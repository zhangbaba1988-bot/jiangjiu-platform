import{_ as f,o as k,a as o,c as n,b as s,t as r,u as $,e as c,g as b}from"./index-DsX0hPjV.js";import{k as h}from"./index-D1BUC7zi.js";const w={class:"article-detail"},y={key:0,class:"state-box"},B={key:1,class:"state-box"},T={class:"error-text"},x={key:2,class:"article-card"},D={class:"article-header"},M={class:"article-icon"},A={class:"article-meta"},G=["innerHTML"],q={__name:"KnowledgeDetail",setup(C){const p=$(),u=c(!0),d=c(null),a=c({title:"加载中...",views:0,content:""}),v=t=>t>=1e4?(t/1e4).toFixed(1)+"万":String(t||0),_=t=>{if(!t||typeof t!="string")return"";let e=t.replace(/^### (.+)$/gm,"<h4>$1</h4>").replace(/^## (.+)$/gm,"<h3>$1</h3>").replace(/\*\*(.+?)\*\*/g,"<strong>$1</strong>").replace(/\*(.+?)\*/g,"<em>$1</em>").replace(/^- (.+)$/gm,"<li>$1</li>").replace(/^\|(.+)\|$/gm,l=>{const g=l.split("|").filter(i=>i.trim());return g.length>=2?'<div class="data-row"><span>'+g.map(i=>i.trim()).join("</span><span>")+"</span></div>":l}).replace(/^\|[-| ]+\|$/gm,"").replace(/^\* (.+)$/gm,"<blockquote>$1</blockquote>").replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>");return e=e.replace(/(<li>.*?<\/li>)/gs,l=>l.includes("</ul>")?l:"<ul>"+l+"</ul>"),e=e.replace(/<p><\/p>/g,""),e=e.replace(/<p><br><\/p>/g,""),"<p>"+e+"</p>"},m=b(()=>_(a.value.content));return k(async()=>{try{const t=await h.getDetail(p.params.id);t.code===200&&t.data?a.value=t.data:a.value={title:"文章不存在",author:"",views:0,content:"抱歉，您访问的文章不存在。"}}catch{const l={klg_043:{id:"klg_043",title:"抖音金黄桶装酱酒是真老酒吗？新国标说清楚了",author:"酱香荟",icon:"🛢️",views:5800,content:`最近很多酒友私信：抖音上透明塑料桶装的酱香酒，颜色金黄透亮，看着像陈年老酒，这种黄是自然的，还是加了东西？

今天结合最新国标GB/T 10781.4-2024，把桶装酱酒颜色猫腻、塑料存酒风险一次性讲透。

## 一、新国标：正宗酱香酒该是什么颜色？

新国标GB/T 10781.4-2024（2025-06-01实施）明确：
- 酱香型白酒：清澈、透明、无色或微黄，无沉淀、无悬浮物
- 严禁添加焦糖色、合成色素、香精、甜味剂
- 不得添加食用酒精及非发酵呈香呈味物质

微黄来自长期储存中天然联酮类物质，随年份缓慢加深：3-5年极淡微黄；10年+略深但依然清亮通透。

**真老酒是清浅微黄，不是深金黄、浓茶黄。**抖音桶装酒那种金黄浓郁，大概率是新酒+人工色素。

## 二、塑料桶装酒：安全隐患

普通塑料桶耐热差，暴晒/高温→塑化剂析出溶进酒里。酱酒活性物质多，长期接触塑料会腐蚀桶壁、带入塑胶臭，破坏酱香层次。存酒应用陶坛、玻璃、食品级不锈钢。

## 三、新国标重点：买酱酒认准这3点

1. **标准号**：2025-06-01后认准GB/T 10781.4-2024
2. **工艺标注**：优选酱香型白酒（大曲），12987工艺
3. **色泽判断**：清澈微黄、通透干净；颜色过黄有塑胶味→直接pass

## 四、总结

颜色≠年份。金黄多是调色，清浅微黄才是真年份本色。坚决不用塑料桶存酒。新国标落地后，无添加、纯固态、工艺透明才是趋势。`}}[p.params.id];l?a.value=l:a.value={title:"文章不存在",author:"",views:0,content:"抱歉，您访问的文章不存在。"}}finally{u.value=!1}}),(t,e)=>(o(),n("div",w,[s("button",{class:"back-btn",onClick:e[0]||(e[0]=l=>t.$router.back())},"← 返回列表"),u.value?(o(),n("div",y,[...e[1]||(e[1]=[s("div",{class:"state-icon"},"⏳",-1),s("p",null,"加载中...",-1)])])):d.value?(o(),n("div",B,[e[2]||(e[2]=s("div",{class:"state-icon"},"⚠️",-1)),s("p",T,r(d.value),1)])):(o(),n("article",x,[s("header",D,[s("span",M,r(a.value.icon||"📖"),1),s("h1",null,r(a.value.title),1),s("div",A,[s("span",null,r(v(a.value.views))+" 阅读",1)])]),s("div",{class:"article-body",innerHTML:m.value},null,8,G),e[3]||(e[3]=s("footer",{class:"article-footer"},null,-1))]))]))}},L=f(q,[["__scopeId","data-v-95f48b66"]]);export{L as default};
