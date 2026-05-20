import{_ as w,o as $,a as o,c,b as t,t as l,F as y,r as x,g as B,h as C,u as T,e as i,i as V}from"./index-DsOHRN2O.js";import{k as q}from"./index-BrWZzSCf.js";const D={class:"article-detail"},M={key:0,class:"state-box"},j={key:1,class:"state-box"},A={class:"error-text"},F={key:2,class:"article-card"},G={class:"article-header"},L={class:"article-icon"},N={class:"article-meta"},H=["innerHTML"],K={class:"cta-section"},S={class:"cta-products"},z={class:"cta-p-icon"},E={class:"cta-p-info"},I={class:"cta-p-price"},P={class:"cta-contact"},R={key:0,class:"cta-contact-info"},J={__name:"KnowledgeDetail",setup(O){const u=T(),p=i(!0),v=i(null),n=i({title:"加载中...",author:"",views:0,content:""}),r=i(!1),_=i([{icon:"🍶",name:"君范·经典酱香",desc:"坤沙工艺 · 5年窖藏 · 53度",price:"¥298/瓶"},{icon:"🏺",name:"君范·陈酿老酒",desc:"10年基酒 · 大师勾调 · 礼盒装",price:"¥688/瓶"},{icon:"👑",name:"君范·珍藏版",desc:"15年老酒 · 限量发售 · 收藏级",price:"¥1688/瓶"}]),m=()=>{r.value=!r.value},f=()=>{window.location.href="/wineries"},b=a=>{if(!a||typeof a!="string")return"";let e=a.replace(/^### (.+)$/gm,"<h4>$1</h4>").replace(/^## (.+)$/gm,"<h3>$1</h3>").replace(/\*\*(.+?)\*\*/g,"<strong>$1</strong>").replace(/\*(.+?)\*/g,"<em>$1</em>").replace(/^- (.+)$/gm,"<li>$1</li>").replace(/^\|(.+)\|$/gm,s=>{const g=s.split("|").filter(d=>d.trim());return g.length>=2?'<div class="data-row"><span>'+g.map(d=>d.trim()).join("</span><span>")+"</span></div>":s}).replace(/^\|[-| ]+\|$/gm,"").replace(/^\* (.+)$/gm,"<blockquote>$1</blockquote>").replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>");return e=e.replace(/(<li>.*?<\/li>)/gs,s=>s.includes("</ul>")?s:"<ul>"+s+"</ul>"),e=e.replace(/<p><\/p>/g,""),e=e.replace(/<p><br><\/p>/g,""),"<p>"+e+"</p>"},k=V(()=>b(n.value.content)),h=a=>a>=1e4?(a/1e4).toFixed(1)+"万":String(a||0);return $(async()=>{try{const a=await q.getDetail(u.params.id);a.code===200&&a.data?n.value=a.data:n.value={title:"文章不存在",author:"",views:0,content:"抱歉，您访问的文章不存在。"}}catch{const s={klg_043:{id:"klg_043",title:"抖音金黄桶装酱酒是真老酒吗？新国标说清楚了",author:"酱香荟",icon:"🛢️",views:5800,content:`最近很多酒友私信：抖音上透明塑料桶装的酱香酒，颜色金黄透亮，看着像陈年老酒，这种黄是自然的，还是加了东西？

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

颜色≠年份。金黄多是调色，清浅微黄才是真年份本色。坚决不用塑料桶存酒。新国标落地后，无添加、纯固态、工艺透明才是趋势。`}}[u.params.id];s?n.value=s:n.value={title:"文章不存在",author:"",views:0,content:"抱歉，您访问的文章不存在。"}}finally{p.value=!1}}),(a,e)=>(o(),c("div",D,[t("button",{class:"back-btn",onClick:e[0]||(e[0]=s=>a.$router.back())},"← 返回列表"),p.value?(o(),c("div",M,[...e[1]||(e[1]=[t("div",{class:"state-icon"},"⏳",-1),t("p",null,"加载中...",-1)])])):v.value?(o(),c("div",j,[e[2]||(e[2]=t("div",{class:"state-icon"},"⚠️",-1)),t("p",A,l(v.value),1)])):(o(),c("article",F,[t("header",G,[t("span",L,l(n.value.icon||"📖"),1),t("h1",null,l(n.value.title),1),t("div",N,[t("span",null,l(n.value.author),1),e[3]||(e[3]=t("span",{class:"dot"},"·",-1)),t("span",null,l(h(n.value.views))+" 阅读",1)])]),t("div",{class:"article-body",innerHTML:k.value},null,8,H),t("div",K,[e[6]||(e[6]=t("div",{class:"cta-divider"},[t("span",null,"📌 酱酒选购指南")],-1)),t("div",S,[(o(!0),c(y,null,x(_.value,s=>(o(),c("div",{class:"cta-product",key:s.name},[t("span",z,l(s.icon),1),t("div",E,[t("strong",null,l(s.name),1),t("span",null,l(s.desc),1)]),t("span",I,l(s.price),1)]))),128))]),t("div",P,[e[5]||(e[5]=t("div",{class:"cta-qr"},[t("span",{class:"cta-qr-icon"},"💬"),t("div",null,[t("strong",null,"想了解更多酱酒知识？"),t("p",null,"扫码添加微信，获取专属选购建议")])],-1)),t("div",{class:"cta-actions"},[t("button",{class:"cta-btn cta-btn-primary",onClick:m},"📱 咨询酱酒选购"),t("button",{class:"cta-btn",onClick:f},"🍶 查看产品")]),r.value?(o(),c("div",R,[...e[4]||(e[4]=[t("p",null,[B("微信号："),t("strong",null,"bingge_jiangjiu")],-1),t("p",{style:{"font-size":"12px",color:"#999"}},'备注"酱酒知识库"优先通过',-1)])])):C("",!0)])]),e[7]||(e[7]=t("footer",{class:"article-footer"},[t("p",null,"* 本文内容综合自茅台官网、中国酒业协会、新华网等权威来源")],-1))]))]))}},W=w(J,[["__scopeId","data-v-eed5ff3d"]]);export{W as default};
