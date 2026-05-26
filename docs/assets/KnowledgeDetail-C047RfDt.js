import{_ as y,o as $,a as l,c as i,b as a,t as o,j as w,e as _,k as h,u as j,r as c,h as x}from"./index-CIdVcbwW.js";import{k as T}from"./index-lgtVnoE6.js";const B="/jiangjiu-platform/qr-wechat.png",V={class:"article-detail"},q={key:0,class:"state-box"},C={key:1,class:"state-box"},D={class:"error-text"},M={key:2,class:"article-card"},N={class:"article-header"},A={class:"article-icon"},G={class:"article-meta"},S=["innerHTML"],H={class:"cta-section"},K={class:"cta-contact"},L={class:"cta-actions"},z={key:0,class:"cta-contact-info"},E={__name:"KnowledgeDetail",setup(F){const d=j(),p=c(!0),v=c(null),n=c({title:"加载中...",views:0,content:""}),u=c(!1),m=()=>{navigator.clipboard.writeText("bingge_jiangjiu").then(()=>{alert("微信号已复制！打开微信搜索添加")}).catch(()=>{alert("微信号：bingge_jiangjiu")})},f=s=>s>=1e4?(s/1e4).toFixed(1)+"万":String(s||0),b=s=>{if(!s||typeof s!="string")return"";let t=s.replace(/^### (.+)$/gm,"<h4>$1</h4>").replace(/^## (.+)$/gm,"<h3>$1</h3>").replace(/\*\*(.+?)\*\*/g,"<strong>$1</strong>").replace(/\*(.+?)\*/g,"<em>$1</em>").replace(/^- (.+)$/gm,"<li>$1</li>").replace(/^\|(.+)\|$/gm,e=>{const g=e.split("|").filter(r=>r.trim());return g.length>=2?'<div class="data-row"><span>'+g.map(r=>r.trim()).join("</span><span>")+"</span></div>":e}).replace(/^\|[-| ]+\|$/gm,"").replace(/^\* (.+)$/gm,"<blockquote>$1</blockquote>").replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>");return t=t.replace(/(<li>.*?<\/li>)/gs,e=>e.includes("</ul>")?e:"<ul>"+e+"</ul>"),t=t.replace(/<p><\/p>/g,""),t=t.replace(/<p><br><\/p>/g,""),"<p>"+t+"</p>"},k=x(()=>b(n.value.content));return $(async()=>{try{const s=await T.getDetail(d.params.id);s.code===200&&s.data?n.value=s.data:n.value={title:"文章不存在",author:"",views:0,content:"抱歉，您访问的文章不存在。"}}catch{const e={klg_043:{id:"klg_043",title:"抖音金黄桶装酱酒是真老酒吗？新国标说清楚了",author:"酱香荟",icon:"🛢️",views:5800,content:`最近很多酒友私信：抖音上透明塑料桶装的酱香酒，颜色金黄透亮，看着像陈年老酒，这种黄是自然的，还是加了东西？

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

颜色≠年份。金黄多是调色，清浅微黄才是真年份本色。坚决不用塑料桶存酒。新国标落地后，无添加、纯固态、工艺透明才是趋势。`}}[d.params.id];e?n.value=e:n.value={title:"文章不存在",author:"",views:0,content:"抱歉，您访问的文章不存在。"}}finally{p.value=!1}}),(s,t)=>(l(),i("div",V,[a("button",{class:"back-btn",onClick:t[0]||(t[0]=e=>s.$router.back())},"← 返回列表"),p.value?(l(),i("div",q,[...t[2]||(t[2]=[a("div",{class:"state-icon"},"⏳",-1),a("p",null,"加载中...",-1)])])):v.value?(l(),i("div",C,[t[3]||(t[3]=a("div",{class:"state-icon"},"⚠️",-1)),a("p",D,o(v.value),1)])):(l(),i("article",M,[a("header",N,[a("span",A,o(n.value.icon||"📖"),1),a("h1",null,o(n.value.title),1),a("div",G,[a("span",null,o(f(n.value.views))+" 阅读",1)])]),a("div",{class:"article-body",innerHTML:k.value},null,8,S),t[4]||(t[4]=a("footer",{class:"article-footer"},null,-1))])),a("div",H,[t[7]||(t[7]=w('<div class="cta-divider" data-v-314aad29><span data-v-314aad29>🍶 想要品鉴正宗酱酒？</span></div><div class="cta-products" data-v-314aad29><div class="cta-product" data-v-314aad29><span class="cta-p-icon" data-v-314aad29>🛢️</span><div class="cta-p-info" data-v-314aad29><strong data-v-314aad29>君范·雅藏 y5</strong><span data-v-314aad29>5年坤沙 · 入门首选</span></div><span class="cta-p-price" data-v-314aad29>¥198/桶</span></div><div class="cta-product" data-v-314aad29><span class="cta-p-icon" data-v-314aad29>🏺</span><div class="cta-p-info" data-v-314aad29><strong data-v-314aad29>君范·典藏 y10</strong><span data-v-314aad29>10年坤沙 · 酒友钟爱</span></div><span class="cta-p-price" data-v-314aad29>¥398/桶</span></div><div class="cta-product" data-v-314aad29><span class="cta-p-icon" data-v-314aad29>👑</span><div class="cta-p-info" data-v-314aad29><strong data-v-314aad29>君范·臻藏 y14</strong><span data-v-314aad29>14年坤沙 · 品鉴级</span></div><span class="cta-p-price" data-v-314aad29>¥698/桶</span></div></div>',2)),a("div",K,[t[6]||(t[6]=a("div",{class:"cta-qr"},[a("img",{src:B,alt:"微信二维码",class:"cta-qr-img"}),a("div",null,[a("strong",null,"👤 兵哥微信号：bingge_jiangjiu"),a("p",null,'加微信备注"知识库"，秒通过')])],-1)),a("div",L,[a("button",{class:"cta-btn",onClick:m},"📋 复制微信号"),a("button",{class:"cta-btn cta-btn-primary",onClick:t[1]||(t[1]=e=>u.value=!0)},"💬 立即咨询")]),u.value?(l(),i("div",z,[...t[5]||(t[5]=[a("p",null,[_("📱 微信搜索："),a("strong",null,"bingge_jiangjiu")],-1),a("p",null,[_("📝 备注："),a("strong",null,"知识库")],-1),a("p",{style:{"margin-top":"6px","font-size":"12px",opacity:".7"}},"或扫描左侧二维码直接添加",-1)])])):h("",!0)])])]))}},W=y(E,[["__scopeId","data-v-314aad29"]]);export{W as default};
