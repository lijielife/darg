/*! jQuery v3.2.1 | (c) JS Foundation and other contributors | jquery.org/license */
!function(a,b){"use strict";"object"==typeof module&&"object"==typeof module.exports?module.exports=a.document?b(a,!0):function(a){if(!a.document)throw new Error("jQuery requires a window with a document");return b(a)}:b(a)}("undefined"!=typeof window?window:this,function(a,b){"use strict";var c=[],d=a.document,e=Object.getPrototypeOf,f=c.slice,g=c.concat,h=c.push,i=c.indexOf,j={},k=j.toString,l=j.hasOwnProperty,m=l.toString,n=m.call(Object),o={};function p(a,b){b=b||d;var c=b.createElement("script");c.text=a,b.head.appendChild(c).parentNode.removeChild(c)}var q="3.2.1",r=function(a,b){return new r.fn.init(a,b)},s=/^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g,t=/^-ms-/,u=/-([a-z])/g,v=function(a,b){return b.toUpperCase()};r.fn=r.prototype={jquery:q,constructor:r,length:0,toArray:function(){return f.call(this)},get:function(a){return null==a?f.call(this):a<0?this[a+this.length]:this[a]},pushStack:function(a){var b=r.merge(this.constructor(),a);return b.prevObject=this,b},each:function(a){return r.each(this,a)},map:function(a){return this.pushStack(r.map(this,function(b,c){return a.call(b,c,b)}))},slice:function(){return this.pushStack(f.apply(this,arguments))},first:function(){return this.eq(0)},last:function(){return this.eq(-1)},eq:function(a){var b=this.length,c=+a+(a<0?b:0);return this.pushStack(c>=0&&c<b?[this[c]]:[])},end:function(){return this.prevObject||this.constructor()},push:h,sort:c.sort,splice:c.splice},r.extend=r.fn.extend=function(){var a,b,c,d,e,f,g=arguments[0]||{},h=1,i=arguments.length,j=!1;for("boolean"==typeof g&&(j=g,g=arguments[h]||{},h++),"object"==typeof g||r.isFunction(g)||(g={}),h===i&&(g=this,h--);h<i;h++)if(null!=(a=arguments[h]))for(b in a)c=g[b],d=a[b],g!==d&&(j&&d&&(r.isPlainObject(d)||(e=Array.isArray(d)))?(e?(e=!1,f=c&&Array.isArray(c)?c:[]):f=c&&r.isPlainObject(c)?c:{},g[b]=r.extend(j,f,d)):void 0!==d&&(g[b]=d));return g},r.extend({expando:"jQuery"+(q+Math.random()).replace(/\D/g,""),isReady:!0,error:function(a){throw new Error(a)},noop:function(){},isFunction:function(a){return"function"===r.type(a)},isWindow:function(a){return null!=a&&a===a.window},isNumeric:function(a){var b=r.type(a);return("number"===b||"string"===b)&&!isNaN(a-parseFloat(a))},isPlainObject:function(a){var b,c;return!(!a||"[object Object]"!==k.call(a))&&(!(b=e(a))||(c=l.call(b,"constructor")&&b.constructor,"function"==typeof c&&m.call(c)===n))},isEmptyObject:function(a){var b;for(b in a)return!1;return!0},type:function(a){return null==a?a+"":"object"==typeof a||"function"==typeof a?j[k.call(a)]||"object":typeof a},globalEval:function(a){p(a)},camelCase:function(a){return a.replace(t,"ms-").replace(u,v)},each:function(a,b){var c,d=0;if(w(a)){for(c=a.length;d<c;d++)if(b.call(a[d],d,a[d])===!1)break}else for(d in a)if(b.call(a[d],d,a[d])===!1)break;return a},trim:function(a){return null==a?"":(a+"").replace(s,"")},makeArray:function(a,b){var c=b||[];return null!=a&&(w(Object(a))?r.merge(c,"string"==typeof a?[a]:a):h.call(c,a)),c},inArray:function(a,b,c){return null==b?-1:i.call(b,a,c)},merge:function(a,b){for(var c=+b.length,d=0,e=a.length;d<c;d++)a[e++]=b[d];return a.length=e,a},grep:function(a,b,c){for(var d,e=[],f=0,g=a.length,h=!c;f<g;f++)d=!b(a[f],f),d!==h&&e.push(a[f]);return e},map:function(a,b,c){var d,e,f=0,h=[];if(w(a))for(d=a.length;f<d;f++)e=b(a[f],f,c),null!=e&&h.push(e);else for(f in a)e=b(a[f],f,c),null!=e&&h.push(e);return g.apply([],h)},guid:1,proxy:function(a,b){var c,d,e;if("string"==typeof b&&(c=a[b],b=a,a=c),r.isFunction(a))return d=f.call(arguments,2),e=function(){return a.apply(b||this,d.concat(f.call(arguments)))},e.guid=a.guid=a.guid||r.guid++,e},now:Date.now,support:o}),"function"==typeof Symbol&&(r.fn[Symbol.iterator]=c[Symbol.iterator]),r.each("Boolean Number String Function Array Date RegExp Object Error Symbol".split(" "),function(a,b){j["[object "+b+"]"]=b.toLowerCase()});function w(a){var b=!!a&&"length"in a&&a.length,c=r.type(a);return"function"!==c&&!r.isWindow(a)&&("array"===c||0===b||"number"==typeof b&&b>0&&b-1 in a)}var x=function(a){var b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u="sizzle"+1*new Date,v=a.document,w=0,x=0,y=ha(),z=ha(),A=ha(),B=function(a,b){return a===b&&(l=!0),0},C={}.hasOwnProperty,D=[],E=D.pop,F=D.push,G=D.push,H=D.slice,I=function(a,b){for(var c=0,d=a.length;c<d;c++)if(a[c]===b)return c;return-1},J="checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|ismap|loop|multiple|open|readonly|required|scoped",K="[\\x20\\t\\r\\n\\f]",L="(?:\\\\.|[\\w-]|[^\0-\\xa0])+",M="\\["+K+"*("+L+")(?:"+K+"*([*^$|!~]?=)"+K+"*(?:'((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\"|("+L+"))|)"+K+"*\\]",N=":("+L+")(?:\\((('((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\")|((?:\\\\.|[^\\\\()[\\]]|"+M+")*)|.*)\\)|)",O=new RegExp(K+"+","g"),P=new RegExp("^"+K+"+|((?:^|[^\\\\])(?:\\\\.)*)"+K+"+$","g"),Q=new RegExp("^"+K+"*,"+K+"*"),R=new RegExp("^"+K+"*([>+~]|"+K+")"+K+"*"),S=new RegExp("="+K+"*([^\\]'\"]*?)"+K+"*\\]","g"),T=new RegExp(N),U=new RegExp("^"+L+"$"),V={ID:new RegExp("^#("+L+")"),CLASS:new RegExp("^\\.("+L+")"),TAG:new RegExp("^("+L+"|[*])"),ATTR:new RegExp("^"+M),PSEUDO:new RegExp("^"+N),CHILD:new RegExp("^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\("+K+"*(even|odd|(([+-]|)(\\d*)n|)"+K+"*(?:([+-]|)"+K+"*(\\d+)|))"+K+"*\\)|)","i"),bool:new RegExp("^(?:"+J+")$","i"),needsContext:new RegExp("^"+K+"*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\("+K+"*((?:-\\d)?\\d*)"+K+"*\\)|)(?=[^-]|$)","i")},W=/^(?:input|select|textarea|button)$/i,X=/^h\d$/i,Y=/^[^{]+\{\s*\[native \w/,Z=/^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,$=/[+~]/,_=new RegExp("\\\\([\\da-f]{1,6}"+K+"?|("+K+")|.)","ig"),aa=function(a,b,c){var d="0x"+b-65536;return d!==d||c?b:d<0?String.fromCharCode(d+65536):String.fromCharCode(d>>10|55296,1023&d|56320)},ba=/([\0-\x1f\x7f]|^-?\d)|^-$|[^\0-\x1f\x7f-\uFFFF\w-]/g,ca=function(a,b){return b?"\0"===a?"\ufffd":a.slice(0,-1)+"\\"+a.charCodeAt(a.length-1).toString(16)+" ":"\\"+a},da=function(){m()},ea=ta(function(a){return a.disabled===!0&&("form"in a||"label"in a)},{dir:"parentNode",next:"legend"});try{G.apply(D=H.call(v.childNodes),v.childNodes),D[v.childNodes.length].nodeType}catch(fa){G={apply:D.length?function(a,b){F.apply(a,H.call(b))}:function(a,b){var c=a.length,d=0;while(a[c++]=b[d++]);a.length=c-1}}}function ga(a,b,d,e){var f,h,j,k,l,o,r,s=b&&b.ownerDocument,w=b?b.nodeType:9;if(d=d||[],"string"!=typeof a||!a||1!==w&&9!==w&&11!==w)return d;if(!e&&((b?b.ownerDocument||b:v)!==n&&m(b),b=b||n,p)){if(11!==w&&(l=Z.exec(a)))if(f=l[1]){if(9===w){if(!(j=b.getElementById(f)))return d;if(j.id===f)return d.push(j),d}else if(s&&(j=s.getElementById(f))&&t(b,j)&&j.id===f)return d.push(j),d}else{if(l[2])return G.apply(d,b.getElementsByTagName(a)),d;if((f=l[3])&&c.getElementsByClassName&&b.getElementsByClassName)return G.apply(d,b.getElementsByClassName(f)),d}if(c.qsa&&!A[a+" "]&&(!q||!q.test(a))){if(1!==w)s=b,r=a;else if("object"!==b.nodeName.toLowerCase()){(k=b.getAttribute("id"))?k=k.replace(ba,ca):b.setAttribute("id",k=u),o=g(a),h=o.length;while(h--)o[h]="#"+k+" "+sa(o[h]);r=o.join(","),s=$.test(a)&&qa(b.parentNode)||b}if(r)try{return G.apply(d,s.querySelectorAll(r)),d}catch(x){}finally{k===u&&b.removeAttribute("id")}}}return i(a.replace(P,"$1"),b,d,e)}function ha(){var a=[];function b(c,e){return a.push(c+" ")>d.cacheLength&&delete b[a.shift()],b[c+" "]=e}return b}function ia(a){return a[u]=!0,a}function ja(a){var b=n.createElement("fieldset");try{return!!a(b)}catch(c){return!1}finally{b.parentNode&&b.parentNode.removeChild(b),b=null}}function ka(a,b){var c=a.split("|"),e=c.length;while(e--)d.attrHandle[c[e]]=b}function la(a,b){var c=b&&a,d=c&&1===a.nodeType&&1===b.nodeType&&a.sourceIndex-b.sourceIndex;if(d)return d;if(c)while(c=c.nextSibling)if(c===b)return-1;return a?1:-1}function ma(a){return function(b){var c=b.nodeName.toLowerCase();return"input"===c&&b.type===a}}function na(a){return function(b){var c=b.nodeName.toLowerCase();return("input"===c||"button"===c)&&b.type===a}}function oa(a){return function(b){return"form"in b?b.parentNode&&b.disabled===!1?"label"in b?"label"in b.parentNode?b.parentNode.disabled===a:b.disabled===a:b.isDisabled===a||b.isDisabled!==!a&&ea(b)===a:b.disabled===a:"label"in b&&b.disabled===a}}function pa(a){return ia(function(b){return b=+b,ia(function(c,d){var e,f=a([],c.length,b),g=f.length;while(g--)c[e=f[g]]&&(c[e]=!(d[e]=c[e]))})})}function qa(a){return a&&"undefined"!=typeof a.getElementsByTagName&&a}c=ga.support={},f=ga.isXML=function(a){var b=a&&(a.ownerDocument||a).documentElement;return!!b&&"HTML"!==b.nodeName},m=ga.setDocument=function(a){var b,e,g=a?a.ownerDocument||a:v;return g!==n&&9===g.nodeType&&g.documentElement?(n=g,o=n.documentElement,p=!f(n),v!==n&&(e=n.defaultView)&&e.top!==e&&(e.addEventListener?e.addEventListener("unload",da,!1):e.attachEvent&&e.attachEvent("onunload",da)),c.attributes=ja(function(a){return a.className="i",!a.getAttribute("className")}),c.getElementsByTagName=ja(function(a){return a.appendChild(n.createComment("")),!a.getElementsByTagName("*").length}),c.getElementsByClassName=Y.test(n.getElementsByClassName),c.getById=ja(function(a){return o.appendChild(a).id=u,!n.getElementsByName||!n.getElementsByName(u).length}),c.getById?(d.filter.ID=function(a){var b=a.replace(_,aa);return function(a){return a.getAttribute("id")===b}},d.find.ID=function(a,b){if("undefined"!=typeof b.getElementById&&p){var c=b.getElementById(a);return c?[c]:[]}}):(d.filter.ID=function(a){var b=a.replace(_,aa);return function(a){var c="undefined"!=typeof a.getAttributeNode&&a.getAttributeNode("id");return c&&c.value===b}},d.find.ID=function(a,b){if("undefined"!=typeof b.getElementById&&p){var c,d,e,f=b.getElementById(a);if(f){if(c=f.getAttributeNode("id"),c&&c.value===a)return[f];e=b.getElementsByName(a),d=0;while(f=e[d++])if(c=f.getAttributeNode("id"),c&&c.value===a)return[f]}return[]}}),d.find.TAG=c.getElementsByTagName?function(a,b){return"undefined"!=typeof b.getElementsByTagName?b.getElementsByTagName(a):c.qsa?b.querySelectorAll(a):void 0}:function(a,b){var c,d=[],e=0,f=b.getElementsByTagName(a);if("*"===a){while(c=f[e++])1===c.nodeType&&d.push(c);return d}return f},d.find.CLASS=c.getElementsByClassName&&function(a,b){if("undefined"!=typeof b.getElementsByClassName&&p)return b.getElementsByClassName(a)},r=[],q=[],(c.qsa=Y.test(n.querySelectorAll))&&(ja(function(a){o.appendChild(a).innerHTML="<a id='"+u+"'></a><select id='"+u+"-\r\\' msallowcapture=''><option selected=''></option></select>",a.querySelectorAll("[msallowcapture^='']").length&&q.push("[*^$]="+K+"*(?:''|\"\")"),a.querySelectorAll("[selected]").length||q.push("\\["+K+"*(?:value|"+J+")"),a.querySelectorAll("[id~="+u+"-]").length||q.push("~="),a.querySelectorAll(":checked").length||q.push(":checked"),a.querySelectorAll("a#"+u+"+*").length||q.push(".#.+[+~]")}),ja(function(a){a.innerHTML="<a href='' disabled='disabled'></a><select disabled='disabled'><option/></select>";var b=n.createElement("input");b.setAttribute("type","hidden"),a.appendChild(b).setAttribute("name","D"),a.querySelectorAll("[name=d]").length&&q.push("name"+K+"*[*^$|!~]?="),2!==a.querySelectorAll(":enabled").length&&q.push(":enabled",":disabled"),o.appendChild(a).disabled=!0,2!==a.querySelectorAll(":disabled").length&&q.push(":enabled",":disabled"),a.querySelectorAll("*,:x"),q.push(",.*:")})),(c.matchesSelector=Y.test(s=o.matches||o.webkitMatchesSelector||o.mozMatchesSelector||o.oMatchesSelector||o.msMatchesSelector))&&ja(function(a){c.disconnectedMatch=s.call(a,"*"),s.call(a,"[s!='']:x"),r.push("!=",N)}),q=q.length&&new RegExp(q.join("|")),r=r.length&&new RegExp(r.join("|")),b=Y.test(o.compareDocumentPosition),t=b||Y.test(o.contains)?function(a,b){var c=9===a.nodeType?a.documentElement:a,d=b&&b.parentNode;return a===d||!(!d||1!==d.nodeType||!(c.contains?c.contains(d):a.compareDocumentPosition&&16&a.compareDocumentPosition(d)))}:function(a,b){if(b)while(b=b.parentNode)if(b===a)return!0;return!1},B=b?function(a,b){if(a===b)return l=!0,0;var d=!a.compareDocumentPosition-!b.compareDocumentPosition;return d?d:(d=(a.ownerDocument||a)===(b.ownerDocument||b)?a.compareDocumentPosition(b):1,1&d||!c.sortDetached&&b.compareDocumentPosition(a)===d?a===n||a.ownerDocument===v&&t(v,a)?-1:b===n||b.ownerDocument===v&&t(v,b)?1:k?I(k,a)-I(k,b):0:4&d?-1:1)}:function(a,b){if(a===b)return l=!0,0;var c,d=0,e=a.parentNode,f=b.parentNode,g=[a],h=[b];if(!e||!f)return a===n?-1:b===n?1:e?-1:f?1:k?I(k,a)-I(k,b):0;if(e===f)return la(a,b);c=a;while(c=c.parentNode)g.unshift(c);c=b;while(c=c.parentNode)h.unshift(c);while(g[d]===h[d])d++;return d?la(g[d],h[d]):g[d]===v?-1:h[d]===v?1:0},n):n},ga.matches=function(a,b){return ga(a,null,null,b)},ga.matchesSelector=function(a,b){if((a.ownerDocument||a)!==n&&m(a),b=b.replace(S,"='$1']"),c.matchesSelector&&p&&!A[b+" "]&&(!r||!r.test(b))&&(!q||!q.test(b)))try{var d=s.call(a,b);if(d||c.disconnectedMatch||a.document&&11!==a.document.nodeType)return d}catch(e){}return ga(b,n,null,[a]).length>0},ga.contains=function(a,b){return(a.ownerDocument||a)!==n&&m(a),t(a,b)},ga.attr=function(a,b){(a.ownerDocument||a)!==n&&m(a);var e=d.attrHandle[b.toLowerCase()],f=e&&C.call(d.attrHandle,b.toLowerCase())?e(a,b,!p):void 0;return void 0!==f?f:c.attributes||!p?a.getAttribute(b):(f=a.getAttributeNode(b))&&f.specified?f.value:null},ga.escape=function(a){return(a+"").replace(ba,ca)},ga.error=function(a){throw new Error("Syntax error, unrecognized expression: "+a)},ga.uniqueSort=function(a){var b,d=[],e=0,f=0;if(l=!c.detectDuplicates,k=!c.sortStable&&a.slice(0),a.sort(B),l){while(b=a[f++])b===a[f]&&(e=d.push(f));while(e--)a.splice(d[e],1)}return k=null,a},e=ga.getText=function(a){var b,c="",d=0,f=a.nodeType;if(f){if(1===f||9===f||11===f){if("string"==typeof a.textContent)return a.textContent;for(a=a.firstChild;a;a=a.nextSibling)c+=e(a)}else if(3===f||4===f)return a.nodeValue}else while(b=a[d++])c+=e(b);return c},d=ga.selectors={cacheLength:50,createPseudo:ia,match:V,attrHandle:{},find:{},relative:{">":{dir:"parentNode",first:!0}," ":{dir:"parentNode"},"+":{dir:"previousSibling",first:!0},"~":{dir:"previousSibling"}},preFilter:{ATTR:function(a){return a[1]=a[1].replace(_,aa),a[3]=(a[3]||a[4]||a[5]||"").replace(_,aa),"~="===a[2]&&(a[3]=" "+a[3]+" "),a.slice(0,4)},CHILD:function(a){return a[1]=a[1].toLowerCase(),"nth"===a[1].slice(0,3)?(a[3]||ga.error(a[0]),a[4]=+(a[4]?a[5]+(a[6]||1):2*("even"===a[3]||"odd"===a[3])),a[5]=+(a[7]+a[8]||"odd"===a[3])):a[3]&&ga.error(a[0]),a},PSEUDO:function(a){var b,c=!a[6]&&a[2];return V.CHILD.test(a[0])?null:(a[3]?a[2]=a[4]||a[5]||"":c&&T.test(c)&&(b=g(c,!0))&&(b=c.indexOf(")",c.length-b)-c.length)&&(a[0]=a[0].slice(0,b),a[2]=c.slice(0,b)),a.slice(0,3))}},filter:{TAG:function(a){var b=a.replace(_,aa).toLowerCase();return"*"===a?function(){return!0}:function(a){return a.nodeName&&a.nodeName.toLowerCase()===b}},CLASS:function(a){var b=y[a+" "];return b||(b=new RegExp("(^|"+K+")"+a+"("+K+"|$)"))&&y(a,function(a){return b.test("string"==typeof a.className&&a.className||"undefined"!=typeof a.getAttribute&&a.getAttribute("class")||"")})},ATTR:function(a,b,c){return function(d){var e=ga.attr(d,a);return null==e?"!="===b:!b||(e+="","="===b?e===c:"!="===b?e!==c:"^="===b?c&&0===e.indexOf(c):"*="===b?c&&e.indexOf(c)>-1:"$="===b?c&&e.slice(-c.length)===c:"~="===b?(" "+e.replace(O," ")+" ").indexOf(c)>-1:"|="===b&&(e===c||e.slice(0,c.length+1)===c+"-"))}},CHILD:function(a,b,c,d,e){var f="nth"!==a.slice(0,3),g="last"!==a.slice(-4),h="of-type"===b;return 1===d&&0===e?function(a){return!!a.parentNode}:function(b,c,i){var j,k,l,m,n,o,p=f!==g?"nextSibling":"previousSibling",q=b.parentNode,r=h&&b.nodeName.toLowerCase(),s=!i&&!h,t=!1;if(q){if(f){while(p){m=b;while(m=m[p])if(h?m.nodeName.toLowerCase()===r:1===m.nodeType)return!1;o=p="only"===a&&!o&&"nextSibling"}return!0}if(o=[g?q.firstChild:q.lastChild],g&&s){m=q,l=m[u]||(m[u]={}),k=l[m.uniqueID]||(l[m.uniqueID]={}),j=k[a]||[],n=j[0]===w&&j[1],t=n&&j[2],m=n&&q.childNodes[n];while(m=++n&&m&&m[p]||(t=n=0)||o.pop())if(1===m.nodeType&&++t&&m===b){k[a]=[w,n,t];break}}else if(s&&(m=b,l=m[u]||(m[u]={}),k=l[m.uniqueID]||(l[m.uniqueID]={}),j=k[a]||[],n=j[0]===w&&j[1],t=n),t===!1)while(m=++n&&m&&m[p]||(t=n=0)||o.pop())if((h?m.nodeName.toLowerCase()===r:1===m.nodeType)&&++t&&(s&&(l=m[u]||(m[u]={}),k=l[m.uniqueID]||(l[m.uniqueID]={}),k[a]=[w,t]),m===b))break;return t-=e,t===d||t%d===0&&t/d>=0}}},PSEUDO:function(a,b){var c,e=d.pseudos[a]||d.setFilters[a.toLowerCase()]||ga.error("unsupported pseudo: "+a);return e[u]?e(b):e.length>1?(c=[a,a,"",b],d.setFilters.hasOwnProperty(a.toLowerCase())?ia(function(a,c){var d,f=e(a,b),g=f.length;while(g--)d=I(a,f[g]),a[d]=!(c[d]=f[g])}):function(a){return e(a,0,c)}):e}},pseudos:{not:ia(function(a){var b=[],c=[],d=h(a.replace(P,"$1"));return d[u]?ia(function(a,b,c,e){var f,g=d(a,null,e,[]),h=a.length;while(h--)(f=g[h])&&(a[h]=!(b[h]=f))}):function(a,e,f){return b[0]=a,d(b,null,f,c),b[0]=null,!c.pop()}}),has:ia(function(a){return function(b){return ga(a,b).length>0}}),contains:ia(function(a){return a=a.replace(_,aa),function(b){return(b.textContent||b.innerText||e(b)).indexOf(a)>-1}}),lang:ia(function(a){return U.test(a||"")||ga.error("unsupported lang: "+a),a=a.replace(_,aa).toLowerCase(),function(b){var c;do if(c=p?b.lang:b.getAttribute("xml:lang")||b.getAttribute("lang"))return c=c.toLowerCase(),c===a||0===c.indexOf(a+"-");while((b=b.parentNode)&&1===b.nodeType);return!1}}),target:function(b){var c=a.location&&a.location.hash;return c&&c.slice(1)===b.id},root:function(a){return a===o},focus:function(a){return a===n.activeElement&&(!n.hasFocus||n.hasFocus())&&!!(a.type||a.href||~a.tabIndex)},enabled:oa(!1),disabled:oa(!0),checked:function(a){var b=a.nodeName.toLowerCase();return"input"===b&&!!a.checked||"option"===b&&!!a.selected},selected:function(a){return a.parentNode&&a.parentNode.selectedIndex,a.selected===!0},empty:function(a){for(a=a.firstChild;a;a=a.nextSibling)if(a.nodeType<6)return!1;return!0},parent:function(a){return!d.pseudos.empty(a)},header:function(a){return X.test(a.nodeName)},input:function(a){return W.test(a.nodeName)},button:function(a){var b=a.nodeName.toLowerCase();return"input"===b&&"button"===a.type||"button"===b},text:function(a){var b;return"input"===a.nodeName.toLowerCase()&&"text"===a.type&&(null==(b=a.getAttribute("type"))||"text"===b.toLowerCase())},first:pa(function(){return[0]}),last:pa(function(a,b){return[b-1]}),eq:pa(function(a,b,c){return[c<0?c+b:c]}),even:pa(function(a,b){for(var c=0;c<b;c+=2)a.push(c);return a}),odd:pa(function(a,b){for(var c=1;c<b;c+=2)a.push(c);return a}),lt:pa(function(a,b,c){for(var d=c<0?c+b:c;--d>=0;)a.push(d);return a}),gt:pa(function(a,b,c){for(var d=c<0?c+b:c;++d<b;)a.push(d);return a})}},d.pseudos.nth=d.pseudos.eq;for(b in{radio:!0,checkbox:!0,file:!0,password:!0,image:!0})d.pseudos[b]=ma(b);for(b in{submit:!0,reset:!0})d.pseudos[b]=na(b);function ra(){}ra.prototype=d.filters=d.pseudos,d.setFilters=new ra,g=ga.tokenize=function(a,b){var c,e,f,g,h,i,j,k=z[a+" "];if(k)return b?0:k.slice(0);h=a,i=[],j=d.preFilter;while(h){c&&!(e=Q.exec(h))||(e&&(h=h.slice(e[0].length)||h),i.push(f=[])),c=!1,(e=R.exec(h))&&(c=e.shift(),f.push({value:c,type:e[0].replace(P," ")}),h=h.slice(c.length));for(g in d.filter)!(e=V[g].exec(h))||j[g]&&!(e=j[g](e))||(c=e.shift(),f.push({value:c,type:g,matches:e}),h=h.slice(c.length));if(!c)break}return b?h.length:h?ga.error(a):z(a,i).slice(0)};function sa(a){for(var b=0,c=a.length,d="";b<c;b++)d+=a[b].value;return d}function ta(a,b,c){var d=b.dir,e=b.next,f=e||d,g=c&&"parentNode"===f,h=x++;return b.first?function(b,c,e){while(b=b[d])if(1===b.nodeType||g)return a(b,c,e);return!1}:function(b,c,i){var j,k,l,m=[w,h];if(i){while(b=b[d])if((1===b.nodeType||g)&&a(b,c,i))return!0}else while(b=b[d])if(1===b.nodeType||g)if(l=b[u]||(b[u]={}),k=l[b.uniqueID]||(l[b.uniqueID]={}),e&&e===b.nodeName.toLowerCase())b=b[d]||b;else{if((j=k[f])&&j[0]===w&&j[1]===h)return m[2]=j[2];if(k[f]=m,m[2]=a(b,c,i))return!0}return!1}}function ua(a){return a.length>1?function(b,c,d){var e=a.length;while(e--)if(!a[e](b,c,d))return!1;return!0}:a[0]}function va(a,b,c){for(var d=0,e=b.length;d<e;d++)ga(a,b[d],c);return c}function wa(a,b,c,d,e){for(var f,g=[],h=0,i=a.length,j=null!=b;h<i;h++)(f=a[h])&&(c&&!c(f,d,e)||(g.push(f),j&&b.push(h)));return g}function xa(a,b,c,d,e,f){return d&&!d[u]&&(d=xa(d)),e&&!e[u]&&(e=xa(e,f)),ia(function(f,g,h,i){var j,k,l,m=[],n=[],o=g.length,p=f||va(b||"*",h.nodeType?[h]:h,[]),q=!a||!f&&b?p:wa(p,m,a,h,i),r=c?e||(f?a:o||d)?[]:g:q;if(c&&c(q,r,h,i),d){j=wa(r,n),d(j,[],h,i),k=j.length;while(k--)(l=j[k])&&(r[n[k]]=!(q[n[k]]=l))}if(f){if(e||a){if(e){j=[],k=r.length;while(k--)(l=r[k])&&j.push(q[k]=l);e(null,r=[],j,i)}k=r.length;while(k--)(l=r[k])&&(j=e?I(f,l):m[k])>-1&&(f[j]=!(g[j]=l))}}else r=wa(r===g?r.splice(o,r.length):r),e?e(null,g,r,i):G.apply(g,r)})}function ya(a){for(var b,c,e,f=a.length,g=d.relative[a[0].type],h=g||d.relative[" "],i=g?1:0,k=ta(function(a){return a===b},h,!0),l=ta(function(a){return I(b,a)>-1},h,!0),m=[function(a,c,d){var e=!g&&(d||c!==j)||((b=c).nodeType?k(a,c,d):l(a,c,d));return b=null,e}];i<f;i++)if(c=d.relative[a[i].type])m=[ta(ua(m),c)];else{if(c=d.filter[a[i].type].apply(null,a[i].matches),c[u]){for(e=++i;e<f;e++)if(d.relative[a[e].type])break;return xa(i>1&&ua(m),i>1&&sa(a.slice(0,i-1).concat({value:" "===a[i-2].type?"*":""})).replace(P,"$1"),c,i<e&&ya(a.slice(i,e)),e<f&&ya(a=a.slice(e)),e<f&&sa(a))}m.push(c)}return ua(m)}function za(a,b){var c=b.length>0,e=a.length>0,f=function(f,g,h,i,k){var l,o,q,r=0,s="0",t=f&&[],u=[],v=j,x=f||e&&d.find.TAG("*",k),y=w+=null==v?1:Math.random()||.1,z=x.length;for(k&&(j=g===n||g||k);s!==z&&null!=(l=x[s]);s++){if(e&&l){o=0,g||l.ownerDocument===n||(m(l),h=!p);while(q=a[o++])if(q(l,g||n,h)){i.push(l);break}k&&(w=y)}c&&((l=!q&&l)&&r--,f&&t.push(l))}if(r+=s,c&&s!==r){o=0;while(q=b[o++])q(t,u,g,h);if(f){if(r>0)while(s--)t[s]||u[s]||(u[s]=E.call(i));u=wa(u)}G.apply(i,u),k&&!f&&u.length>0&&r+b.length>1&&ga.uniqueSort(i)}return k&&(w=y,j=v),t};return c?ia(f):f}return h=ga.compile=function(a,b){var c,d=[],e=[],f=A[a+" "];if(!f){b||(b=g(a)),c=b.length;while(c--)f=ya(b[c]),f[u]?d.push(f):e.push(f);f=A(a,za(e,d)),f.selector=a}return f},i=ga.select=function(a,b,c,e){var f,i,j,k,l,m="function"==typeof a&&a,n=!e&&g(a=m.selector||a);if(c=c||[],1===n.length){if(i=n[0]=n[0].slice(0),i.length>2&&"ID"===(j=i[0]).type&&9===b.nodeType&&p&&d.relative[i[1].type]){if(b=(d.find.ID(j.matches[0].replace(_,aa),b)||[])[0],!b)return c;m&&(b=b.parentNode),a=a.slice(i.shift().value.length)}f=V.needsContext.test(a)?0:i.length;while(f--){if(j=i[f],d.relative[k=j.type])break;if((l=d.find[k])&&(e=l(j.matches[0].replace(_,aa),$.test(i[0].type)&&qa(b.parentNode)||b))){if(i.splice(f,1),a=e.length&&sa(i),!a)return G.apply(c,e),c;break}}}return(m||h(a,n))(e,b,!p,c,!b||$.test(a)&&qa(b.parentNode)||b),c},c.sortStable=u.split("").sort(B).join("")===u,c.detectDuplicates=!!l,m(),c.sortDetached=ja(function(a){return 1&a.compareDocumentPosition(n.createElement("fieldset"))}),ja(function(a){return a.innerHTML="<a href='#'></a>","#"===a.firstChild.getAttribute("href")})||ka("type|href|height|width",function(a,b,c){if(!c)return a.getAttribute(b,"type"===b.toLowerCase()?1:2)}),c.attributes&&ja(function(a){return a.innerHTML="<input/>",a.firstChild.setAttribute("value",""),""===a.firstChild.getAttribute("value")})||ka("value",function(a,b,c){if(!c&&"input"===a.nodeName.toLowerCase())return a.defaultValue}),ja(function(a){return null==a.getAttribute("disabled")})||ka(J,function(a,b,c){var d;if(!c)return a[b]===!0?b.toLowerCase():(d=a.getAttributeNode(b))&&d.specified?d.value:null}),ga}(a);r.find=x,r.expr=x.selectors,r.expr[":"]=r.expr.pseudos,r.uniqueSort=r.unique=x.uniqueSort,r.text=x.getText,r.isXMLDoc=x.isXML,r.contains=x.contains,r.escapeSelector=x.escape;var y=function(a,b,c){var d=[],e=void 0!==c;while((a=a[b])&&9!==a.nodeType)if(1===a.nodeType){if(e&&r(a).is(c))break;d.push(a)}return d},z=function(a,b){for(var c=[];a;a=a.nextSibling)1===a.nodeType&&a!==b&&c.push(a);return c},A=r.expr.match.needsContext;function B(a,b){return a.nodeName&&a.nodeName.toLowerCase()===b.toLowerCase()}var C=/^<([a-z][^\/\0>:\x20\t\r\n\f]*)[\x20\t\r\n\f]*\/?>(?:<\/\1>|)$/i,D=/^.[^:#\[\.,]*$/;function E(a,b,c){return r.isFunction(b)?r.grep(a,function(a,d){return!!b.call(a,d,a)!==c}):b.nodeType?r.grep(a,function(a){return a===b!==c}):"string"!=typeof b?r.grep(a,function(a){return i.call(b,a)>-1!==c}):D.test(b)?r.filter(b,a,c):(b=r.filter(b,a),r.grep(a,function(a){return i.call(b,a)>-1!==c&&1===a.nodeType}))}r.filter=function(a,b,c){var d=b[0];return c&&(a=":not("+a+")"),1===b.length&&1===d.nodeType?r.find.matchesSelector(d,a)?[d]:[]:r.find.matches(a,r.grep(b,function(a){return 1===a.nodeType}))},r.fn.extend({find:function(a){var b,c,d=this.length,e=this;if("string"!=typeof a)return this.pushStack(r(a).filter(function(){for(b=0;b<d;b++)if(r.contains(e[b],this))return!0}));for(c=this.pushStack([]),b=0;b<d;b++)r.find(a,e[b],c);return d>1?r.uniqueSort(c):c},filter:function(a){return this.pushStack(E(this,a||[],!1))},not:function(a){return this.pushStack(E(this,a||[],!0))},is:function(a){return!!E(this,"string"==typeof a&&A.test(a)?r(a):a||[],!1).length}});var F,G=/^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]+))$/,H=r.fn.init=function(a,b,c){var e,f;if(!a)return this;if(c=c||F,"string"==typeof a){if(e="<"===a[0]&&">"===a[a.length-1]&&a.length>=3?[null,a,null]:G.exec(a),!e||!e[1]&&b)return!b||b.jquery?(b||c).find(a):this.constructor(b).find(a);if(e[1]){if(b=b instanceof r?b[0]:b,r.merge(this,r.parseHTML(e[1],b&&b.nodeType?b.ownerDocument||b:d,!0)),C.test(e[1])&&r.isPlainObject(b))for(e in b)r.isFunction(this[e])?this[e](b[e]):this.attr(e,b[e]);return this}return f=d.getElementById(e[2]),f&&(this[0]=f,this.length=1),this}return a.nodeType?(this[0]=a,this.length=1,this):r.isFunction(a)?void 0!==c.ready?c.ready(a):a(r):r.makeArray(a,this)};H.prototype=r.fn,F=r(d);var I=/^(?:parents|prev(?:Until|All))/,J={children:!0,contents:!0,next:!0,prev:!0};r.fn.extend({has:function(a){var b=r(a,this),c=b.length;return this.filter(function(){for(var a=0;a<c;a++)if(r.contains(this,b[a]))return!0})},closest:function(a,b){var c,d=0,e=this.length,f=[],g="string"!=typeof a&&r(a);if(!A.test(a))for(;d<e;d++)for(c=this[d];c&&c!==b;c=c.parentNode)if(c.nodeType<11&&(g?g.index(c)>-1:1===c.nodeType&&r.find.matchesSelector(c,a))){f.push(c);break}return this.pushStack(f.length>1?r.uniqueSort(f):f)},index:function(a){return a?"string"==typeof a?i.call(r(a),this[0]):i.call(this,a.jquery?a[0]:a):this[0]&&this[0].parentNode?this.first().prevAll().length:-1},add:function(a,b){return this.pushStack(r.uniqueSort(r.merge(this.get(),r(a,b))))},addBack:function(a){return this.add(null==a?this.prevObject:this.prevObject.filter(a))}});function K(a,b){while((a=a[b])&&1!==a.nodeType);return a}r.each({parent:function(a){var b=a.parentNode;return b&&11!==b.nodeType?b:null},parents:function(a){return y(a,"parentNode")},parentsUntil:function(a,b,c){return y(a,"parentNode",c)},next:function(a){return K(a,"nextSibling")},prev:function(a){return K(a,"previousSibling")},nextAll:function(a){return y(a,"nextSibling")},prevAll:function(a){return y(a,"previousSibling")},nextUntil:function(a,b,c){return y(a,"nextSibling",c)},prevUntil:function(a,b,c){return y(a,"previousSibling",c)},siblings:function(a){return z((a.parentNode||{}).firstChild,a)},children:function(a){return z(a.firstChild)},contents:function(a){return B(a,"iframe")?a.contentDocument:(B(a,"template")&&(a=a.content||a),r.merge([],a.childNodes))}},function(a,b){r.fn[a]=function(c,d){var e=r.map(this,b,c);return"Until"!==a.slice(-5)&&(d=c),d&&"string"==typeof d&&(e=r.filter(d,e)),this.length>1&&(J[a]||r.uniqueSort(e),I.test(a)&&e.reverse()),this.pushStack(e)}});var L=/[^\x20\t\r\n\f]+/g;function M(a){var b={};return r.each(a.match(L)||[],function(a,c){b[c]=!0}),b}r.Callbacks=function(a){a="string"==typeof a?M(a):r.extend({},a);var b,c,d,e,f=[],g=[],h=-1,i=function(){for(e=e||a.once,d=b=!0;g.length;h=-1){c=g.shift();while(++h<f.length)f[h].apply(c[0],c[1])===!1&&a.stopOnFalse&&(h=f.length,c=!1)}a.memory||(c=!1),b=!1,e&&(f=c?[]:"")},j={add:function(){return f&&(c&&!b&&(h=f.length-1,g.push(c)),function d(b){r.each(b,function(b,c){r.isFunction(c)?a.unique&&j.has(c)||f.push(c):c&&c.length&&"string"!==r.type(c)&&d(c)})}(arguments),c&&!b&&i()),this},remove:function(){return r.each(arguments,function(a,b){var c;while((c=r.inArray(b,f,c))>-1)f.splice(c,1),c<=h&&h--}),this},has:function(a){return a?r.inArray(a,f)>-1:f.length>0},empty:function(){return f&&(f=[]),this},disable:function(){return e=g=[],f=c="",this},disabled:function(){return!f},lock:function(){return e=g=[],c||b||(f=c=""),this},locked:function(){return!!e},fireWith:function(a,c){return e||(c=c||[],c=[a,c.slice?c.slice():c],g.push(c),b||i()),this},fire:function(){return j.fireWith(this,arguments),this},fired:function(){return!!d}};return j};function N(a){return a}function O(a){throw a}function P(a,b,c,d){var e;try{a&&r.isFunction(e=a.promise)?e.call(a).done(b).fail(c):a&&r.isFunction(e=a.then)?e.call(a,b,c):b.apply(void 0,[a].slice(d))}catch(a){c.apply(void 0,[a])}}r.extend({Deferred:function(b){var c=[["notify","progress",r.Callbacks("memory"),r.Callbacks("memory"),2],["resolve","done",r.Callbacks("once memory"),r.Callbacks("once memory"),0,"resolved"],["reject","fail",r.Callbacks("once memory"),r.Callbacks("once memory"),1,"rejected"]],d="pending",e={state:function(){return d},always:function(){return f.done(arguments).fail(arguments),this},"catch":function(a){return e.then(null,a)},pipe:function(){var a=arguments;return r.Deferred(function(b){r.each(c,function(c,d){var e=r.isFunction(a[d[4]])&&a[d[4]];f[d[1]](function(){var a=e&&e.apply(this,arguments);a&&r.isFunction(a.promise)?a.promise().progress(b.notify).done(b.resolve).fail(b.reject):b[d[0]+"With"](this,e?[a]:arguments)})}),a=null}).promise()},then:function(b,d,e){var f=0;function g(b,c,d,e){return function(){var h=this,i=arguments,j=function(){var a,j;if(!(b<f)){if(a=d.apply(h,i),a===c.promise())throw new TypeError("Thenable self-resolution");j=a&&("object"==typeof a||"function"==typeof a)&&a.then,r.isFunction(j)?e?j.call(a,g(f,c,N,e),g(f,c,O,e)):(f++,j.call(a,g(f,c,N,e),g(f,c,O,e),g(f,c,N,c.notifyWith))):(d!==N&&(h=void 0,i=[a]),(e||c.resolveWith)(h,i))}},k=e?j:function(){try{j()}catch(a){r.Deferred.exceptionHook&&r.Deferred.exceptionHook(a,k.stackTrace),b+1>=f&&(d!==O&&(h=void 0,i=[a]),c.rejectWith(h,i))}};b?k():(r.Deferred.getStackHook&&(k.stackTrace=r.Deferred.getStackHook()),a.setTimeout(k))}}return r.Deferred(function(a){c[0][3].add(g(0,a,r.isFunction(e)?e:N,a.notifyWith)),c[1][3].add(g(0,a,r.isFunction(b)?b:N)),c[2][3].add(g(0,a,r.isFunction(d)?d:O))}).promise()},promise:function(a){return null!=a?r.extend(a,e):e}},f={};return r.each(c,function(a,b){var g=b[2],h=b[5];e[b[1]]=g.add,h&&g.add(function(){d=h},c[3-a][2].disable,c[0][2].lock),g.add(b[3].fire),f[b[0]]=function(){return f[b[0]+"With"](this===f?void 0:this,arguments),this},f[b[0]+"With"]=g.fireWith}),e.promise(f),b&&b.call(f,f),f},when:function(a){var b=arguments.length,c=b,d=Array(c),e=f.call(arguments),g=r.Deferred(),h=function(a){return function(c){d[a]=this,e[a]=arguments.length>1?f.call(arguments):c,--b||g.resolveWith(d,e)}};if(b<=1&&(P(a,g.done(h(c)).resolve,g.reject,!b),"pending"===g.state()||r.isFunction(e[c]&&e[c].then)))return g.then();while(c--)P(e[c],h(c),g.reject);return g.promise()}});var Q=/^(Eval|Internal|Range|Reference|Syntax|Type|URI)Error$/;r.Deferred.exceptionHook=function(b,c){a.console&&a.console.warn&&b&&Q.test(b.name)&&a.console.warn("jQuery.Deferred exception: "+b.message,b.stack,c)},r.readyException=function(b){a.setTimeout(function(){throw b})};var R=r.Deferred();r.fn.ready=function(a){return R.then(a)["catch"](function(a){r.readyException(a)}),this},r.extend({isReady:!1,readyWait:1,ready:function(a){(a===!0?--r.readyWait:r.isReady)||(r.isReady=!0,a!==!0&&--r.readyWait>0||R.resolveWith(d,[r]))}}),r.ready.then=R.then;function S(){d.removeEventListener("DOMContentLoaded",S),
a.removeEventListener("load",S),r.ready()}"complete"===d.readyState||"loading"!==d.readyState&&!d.documentElement.doScroll?a.setTimeout(r.ready):(d.addEventListener("DOMContentLoaded",S),a.addEventListener("load",S));var T=function(a,b,c,d,e,f,g){var h=0,i=a.length,j=null==c;if("object"===r.type(c)){e=!0;for(h in c)T(a,b,h,c[h],!0,f,g)}else if(void 0!==d&&(e=!0,r.isFunction(d)||(g=!0),j&&(g?(b.call(a,d),b=null):(j=b,b=function(a,b,c){return j.call(r(a),c)})),b))for(;h<i;h++)b(a[h],c,g?d:d.call(a[h],h,b(a[h],c)));return e?a:j?b.call(a):i?b(a[0],c):f},U=function(a){return 1===a.nodeType||9===a.nodeType||!+a.nodeType};function V(){this.expando=r.expando+V.uid++}V.uid=1,V.prototype={cache:function(a){var b=a[this.expando];return b||(b={},U(a)&&(a.nodeType?a[this.expando]=b:Object.defineProperty(a,this.expando,{value:b,configurable:!0}))),b},set:function(a,b,c){var d,e=this.cache(a);if("string"==typeof b)e[r.camelCase(b)]=c;else for(d in b)e[r.camelCase(d)]=b[d];return e},get:function(a,b){return void 0===b?this.cache(a):a[this.expando]&&a[this.expando][r.camelCase(b)]},access:function(a,b,c){return void 0===b||b&&"string"==typeof b&&void 0===c?this.get(a,b):(this.set(a,b,c),void 0!==c?c:b)},remove:function(a,b){var c,d=a[this.expando];if(void 0!==d){if(void 0!==b){Array.isArray(b)?b=b.map(r.camelCase):(b=r.camelCase(b),b=b in d?[b]:b.match(L)||[]),c=b.length;while(c--)delete d[b[c]]}(void 0===b||r.isEmptyObject(d))&&(a.nodeType?a[this.expando]=void 0:delete a[this.expando])}},hasData:function(a){var b=a[this.expando];return void 0!==b&&!r.isEmptyObject(b)}};var W=new V,X=new V,Y=/^(?:\{[\w\W]*\}|\[[\w\W]*\])$/,Z=/[A-Z]/g;function $(a){return"true"===a||"false"!==a&&("null"===a?null:a===+a+""?+a:Y.test(a)?JSON.parse(a):a)}function _(a,b,c){var d;if(void 0===c&&1===a.nodeType)if(d="data-"+b.replace(Z,"-$&").toLowerCase(),c=a.getAttribute(d),"string"==typeof c){try{c=$(c)}catch(e){}X.set(a,b,c)}else c=void 0;return c}r.extend({hasData:function(a){return X.hasData(a)||W.hasData(a)},data:function(a,b,c){return X.access(a,b,c)},removeData:function(a,b){X.remove(a,b)},_data:function(a,b,c){return W.access(a,b,c)},_removeData:function(a,b){W.remove(a,b)}}),r.fn.extend({data:function(a,b){var c,d,e,f=this[0],g=f&&f.attributes;if(void 0===a){if(this.length&&(e=X.get(f),1===f.nodeType&&!W.get(f,"hasDataAttrs"))){c=g.length;while(c--)g[c]&&(d=g[c].name,0===d.indexOf("data-")&&(d=r.camelCase(d.slice(5)),_(f,d,e[d])));W.set(f,"hasDataAttrs",!0)}return e}return"object"==typeof a?this.each(function(){X.set(this,a)}):T(this,function(b){var c;if(f&&void 0===b){if(c=X.get(f,a),void 0!==c)return c;if(c=_(f,a),void 0!==c)return c}else this.each(function(){X.set(this,a,b)})},null,b,arguments.length>1,null,!0)},removeData:function(a){return this.each(function(){X.remove(this,a)})}}),r.extend({queue:function(a,b,c){var d;if(a)return b=(b||"fx")+"queue",d=W.get(a,b),c&&(!d||Array.isArray(c)?d=W.access(a,b,r.makeArray(c)):d.push(c)),d||[]},dequeue:function(a,b){b=b||"fx";var c=r.queue(a,b),d=c.length,e=c.shift(),f=r._queueHooks(a,b),g=function(){r.dequeue(a,b)};"inprogress"===e&&(e=c.shift(),d--),e&&("fx"===b&&c.unshift("inprogress"),delete f.stop,e.call(a,g,f)),!d&&f&&f.empty.fire()},_queueHooks:function(a,b){var c=b+"queueHooks";return W.get(a,c)||W.access(a,c,{empty:r.Callbacks("once memory").add(function(){W.remove(a,[b+"queue",c])})})}}),r.fn.extend({queue:function(a,b){var c=2;return"string"!=typeof a&&(b=a,a="fx",c--),arguments.length<c?r.queue(this[0],a):void 0===b?this:this.each(function(){var c=r.queue(this,a,b);r._queueHooks(this,a),"fx"===a&&"inprogress"!==c[0]&&r.dequeue(this,a)})},dequeue:function(a){return this.each(function(){r.dequeue(this,a)})},clearQueue:function(a){return this.queue(a||"fx",[])},promise:function(a,b){var c,d=1,e=r.Deferred(),f=this,g=this.length,h=function(){--d||e.resolveWith(f,[f])};"string"!=typeof a&&(b=a,a=void 0),a=a||"fx";while(g--)c=W.get(f[g],a+"queueHooks"),c&&c.empty&&(d++,c.empty.add(h));return h(),e.promise(b)}});var aa=/[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/.source,ba=new RegExp("^(?:([+-])=|)("+aa+")([a-z%]*)$","i"),ca=["Top","Right","Bottom","Left"],da=function(a,b){return a=b||a,"none"===a.style.display||""===a.style.display&&r.contains(a.ownerDocument,a)&&"none"===r.css(a,"display")},ea=function(a,b,c,d){var e,f,g={};for(f in b)g[f]=a.style[f],a.style[f]=b[f];e=c.apply(a,d||[]);for(f in b)a.style[f]=g[f];return e};function fa(a,b,c,d){var e,f=1,g=20,h=d?function(){return d.cur()}:function(){return r.css(a,b,"")},i=h(),j=c&&c[3]||(r.cssNumber[b]?"":"px"),k=(r.cssNumber[b]||"px"!==j&&+i)&&ba.exec(r.css(a,b));if(k&&k[3]!==j){j=j||k[3],c=c||[],k=+i||1;do f=f||".5",k/=f,r.style(a,b,k+j);while(f!==(f=h()/i)&&1!==f&&--g)}return c&&(k=+k||+i||0,e=c[1]?k+(c[1]+1)*c[2]:+c[2],d&&(d.unit=j,d.start=k,d.end=e)),e}var ga={};function ha(a){var b,c=a.ownerDocument,d=a.nodeName,e=ga[d];return e?e:(b=c.body.appendChild(c.createElement(d)),e=r.css(b,"display"),b.parentNode.removeChild(b),"none"===e&&(e="block"),ga[d]=e,e)}function ia(a,b){for(var c,d,e=[],f=0,g=a.length;f<g;f++)d=a[f],d.style&&(c=d.style.display,b?("none"===c&&(e[f]=W.get(d,"display")||null,e[f]||(d.style.display="")),""===d.style.display&&da(d)&&(e[f]=ha(d))):"none"!==c&&(e[f]="none",W.set(d,"display",c)));for(f=0;f<g;f++)null!=e[f]&&(a[f].style.display=e[f]);return a}r.fn.extend({show:function(){return ia(this,!0)},hide:function(){return ia(this)},toggle:function(a){return"boolean"==typeof a?a?this.show():this.hide():this.each(function(){da(this)?r(this).show():r(this).hide()})}});var ja=/^(?:checkbox|radio)$/i,ka=/<([a-z][^\/\0>\x20\t\r\n\f]+)/i,la=/^$|\/(?:java|ecma)script/i,ma={option:[1,"<select multiple='multiple'>","</select>"],thead:[1,"<table>","</table>"],col:[2,"<table><colgroup>","</colgroup></table>"],tr:[2,"<table><tbody>","</tbody></table>"],td:[3,"<table><tbody><tr>","</tr></tbody></table>"],_default:[0,"",""]};ma.optgroup=ma.option,ma.tbody=ma.tfoot=ma.colgroup=ma.caption=ma.thead,ma.th=ma.td;function na(a,b){var c;return c="undefined"!=typeof a.getElementsByTagName?a.getElementsByTagName(b||"*"):"undefined"!=typeof a.querySelectorAll?a.querySelectorAll(b||"*"):[],void 0===b||b&&B(a,b)?r.merge([a],c):c}function oa(a,b){for(var c=0,d=a.length;c<d;c++)W.set(a[c],"globalEval",!b||W.get(b[c],"globalEval"))}var pa=/<|&#?\w+;/;function qa(a,b,c,d,e){for(var f,g,h,i,j,k,l=b.createDocumentFragment(),m=[],n=0,o=a.length;n<o;n++)if(f=a[n],f||0===f)if("object"===r.type(f))r.merge(m,f.nodeType?[f]:f);else if(pa.test(f)){g=g||l.appendChild(b.createElement("div")),h=(ka.exec(f)||["",""])[1].toLowerCase(),i=ma[h]||ma._default,g.innerHTML=i[1]+r.htmlPrefilter(f)+i[2],k=i[0];while(k--)g=g.lastChild;r.merge(m,g.childNodes),g=l.firstChild,g.textContent=""}else m.push(b.createTextNode(f));l.textContent="",n=0;while(f=m[n++])if(d&&r.inArray(f,d)>-1)e&&e.push(f);else if(j=r.contains(f.ownerDocument,f),g=na(l.appendChild(f),"script"),j&&oa(g),c){k=0;while(f=g[k++])la.test(f.type||"")&&c.push(f)}return l}!function(){var a=d.createDocumentFragment(),b=a.appendChild(d.createElement("div")),c=d.createElement("input");c.setAttribute("type","radio"),c.setAttribute("checked","checked"),c.setAttribute("name","t"),b.appendChild(c),o.checkClone=b.cloneNode(!0).cloneNode(!0).lastChild.checked,b.innerHTML="<textarea>x</textarea>",o.noCloneChecked=!!b.cloneNode(!0).lastChild.defaultValue}();var ra=d.documentElement,sa=/^key/,ta=/^(?:mouse|pointer|contextmenu|drag|drop)|click/,ua=/^([^.]*)(?:\.(.+)|)/;function va(){return!0}function wa(){return!1}function xa(){try{return d.activeElement}catch(a){}}function ya(a,b,c,d,e,f){var g,h;if("object"==typeof b){"string"!=typeof c&&(d=d||c,c=void 0);for(h in b)ya(a,h,c,d,b[h],f);return a}if(null==d&&null==e?(e=c,d=c=void 0):null==e&&("string"==typeof c?(e=d,d=void 0):(e=d,d=c,c=void 0)),e===!1)e=wa;else if(!e)return a;return 1===f&&(g=e,e=function(a){return r().off(a),g.apply(this,arguments)},e.guid=g.guid||(g.guid=r.guid++)),a.each(function(){r.event.add(this,b,e,d,c)})}r.event={global:{},add:function(a,b,c,d,e){var f,g,h,i,j,k,l,m,n,o,p,q=W.get(a);if(q){c.handler&&(f=c,c=f.handler,e=f.selector),e&&r.find.matchesSelector(ra,e),c.guid||(c.guid=r.guid++),(i=q.events)||(i=q.events={}),(g=q.handle)||(g=q.handle=function(b){return"undefined"!=typeof r&&r.event.triggered!==b.type?r.event.dispatch.apply(a,arguments):void 0}),b=(b||"").match(L)||[""],j=b.length;while(j--)h=ua.exec(b[j])||[],n=p=h[1],o=(h[2]||"").split(".").sort(),n&&(l=r.event.special[n]||{},n=(e?l.delegateType:l.bindType)||n,l=r.event.special[n]||{},k=r.extend({type:n,origType:p,data:d,handler:c,guid:c.guid,selector:e,needsContext:e&&r.expr.match.needsContext.test(e),namespace:o.join(".")},f),(m=i[n])||(m=i[n]=[],m.delegateCount=0,l.setup&&l.setup.call(a,d,o,g)!==!1||a.addEventListener&&a.addEventListener(n,g)),l.add&&(l.add.call(a,k),k.handler.guid||(k.handler.guid=c.guid)),e?m.splice(m.delegateCount++,0,k):m.push(k),r.event.global[n]=!0)}},remove:function(a,b,c,d,e){var f,g,h,i,j,k,l,m,n,o,p,q=W.hasData(a)&&W.get(a);if(q&&(i=q.events)){b=(b||"").match(L)||[""],j=b.length;while(j--)if(h=ua.exec(b[j])||[],n=p=h[1],o=(h[2]||"").split(".").sort(),n){l=r.event.special[n]||{},n=(d?l.delegateType:l.bindType)||n,m=i[n]||[],h=h[2]&&new RegExp("(^|\\.)"+o.join("\\.(?:.*\\.|)")+"(\\.|$)"),g=f=m.length;while(f--)k=m[f],!e&&p!==k.origType||c&&c.guid!==k.guid||h&&!h.test(k.namespace)||d&&d!==k.selector&&("**"!==d||!k.selector)||(m.splice(f,1),k.selector&&m.delegateCount--,l.remove&&l.remove.call(a,k));g&&!m.length&&(l.teardown&&l.teardown.call(a,o,q.handle)!==!1||r.removeEvent(a,n,q.handle),delete i[n])}else for(n in i)r.event.remove(a,n+b[j],c,d,!0);r.isEmptyObject(i)&&W.remove(a,"handle events")}},dispatch:function(a){var b=r.event.fix(a),c,d,e,f,g,h,i=new Array(arguments.length),j=(W.get(this,"events")||{})[b.type]||[],k=r.event.special[b.type]||{};for(i[0]=b,c=1;c<arguments.length;c++)i[c]=arguments[c];if(b.delegateTarget=this,!k.preDispatch||k.preDispatch.call(this,b)!==!1){h=r.event.handlers.call(this,b,j),c=0;while((f=h[c++])&&!b.isPropagationStopped()){b.currentTarget=f.elem,d=0;while((g=f.handlers[d++])&&!b.isImmediatePropagationStopped())b.rnamespace&&!b.rnamespace.test(g.namespace)||(b.handleObj=g,b.data=g.data,e=((r.event.special[g.origType]||{}).handle||g.handler).apply(f.elem,i),void 0!==e&&(b.result=e)===!1&&(b.preventDefault(),b.stopPropagation()))}return k.postDispatch&&k.postDispatch.call(this,b),b.result}},handlers:function(a,b){var c,d,e,f,g,h=[],i=b.delegateCount,j=a.target;if(i&&j.nodeType&&!("click"===a.type&&a.button>=1))for(;j!==this;j=j.parentNode||this)if(1===j.nodeType&&("click"!==a.type||j.disabled!==!0)){for(f=[],g={},c=0;c<i;c++)d=b[c],e=d.selector+" ",void 0===g[e]&&(g[e]=d.needsContext?r(e,this).index(j)>-1:r.find(e,this,null,[j]).length),g[e]&&f.push(d);f.length&&h.push({elem:j,handlers:f})}return j=this,i<b.length&&h.push({elem:j,handlers:b.slice(i)}),h},addProp:function(a,b){Object.defineProperty(r.Event.prototype,a,{enumerable:!0,configurable:!0,get:r.isFunction(b)?function(){if(this.originalEvent)return b(this.originalEvent)}:function(){if(this.originalEvent)return this.originalEvent[a]},set:function(b){Object.defineProperty(this,a,{enumerable:!0,configurable:!0,writable:!0,value:b})}})},fix:function(a){return a[r.expando]?a:new r.Event(a)},special:{load:{noBubble:!0},focus:{trigger:function(){if(this!==xa()&&this.focus)return this.focus(),!1},delegateType:"focusin"},blur:{trigger:function(){if(this===xa()&&this.blur)return this.blur(),!1},delegateType:"focusout"},click:{trigger:function(){if("checkbox"===this.type&&this.click&&B(this,"input"))return this.click(),!1},_default:function(a){return B(a.target,"a")}},beforeunload:{postDispatch:function(a){void 0!==a.result&&a.originalEvent&&(a.originalEvent.returnValue=a.result)}}}},r.removeEvent=function(a,b,c){a.removeEventListener&&a.removeEventListener(b,c)},r.Event=function(a,b){return this instanceof r.Event?(a&&a.type?(this.originalEvent=a,this.type=a.type,this.isDefaultPrevented=a.defaultPrevented||void 0===a.defaultPrevented&&a.returnValue===!1?va:wa,this.target=a.target&&3===a.target.nodeType?a.target.parentNode:a.target,this.currentTarget=a.currentTarget,this.relatedTarget=a.relatedTarget):this.type=a,b&&r.extend(this,b),this.timeStamp=a&&a.timeStamp||r.now(),void(this[r.expando]=!0)):new r.Event(a,b)},r.Event.prototype={constructor:r.Event,isDefaultPrevented:wa,isPropagationStopped:wa,isImmediatePropagationStopped:wa,isSimulated:!1,preventDefault:function(){var a=this.originalEvent;this.isDefaultPrevented=va,a&&!this.isSimulated&&a.preventDefault()},stopPropagation:function(){var a=this.originalEvent;this.isPropagationStopped=va,a&&!this.isSimulated&&a.stopPropagation()},stopImmediatePropagation:function(){var a=this.originalEvent;this.isImmediatePropagationStopped=va,a&&!this.isSimulated&&a.stopImmediatePropagation(),this.stopPropagation()}},r.each({altKey:!0,bubbles:!0,cancelable:!0,changedTouches:!0,ctrlKey:!0,detail:!0,eventPhase:!0,metaKey:!0,pageX:!0,pageY:!0,shiftKey:!0,view:!0,"char":!0,charCode:!0,key:!0,keyCode:!0,button:!0,buttons:!0,clientX:!0,clientY:!0,offsetX:!0,offsetY:!0,pointerId:!0,pointerType:!0,screenX:!0,screenY:!0,targetTouches:!0,toElement:!0,touches:!0,which:function(a){var b=a.button;return null==a.which&&sa.test(a.type)?null!=a.charCode?a.charCode:a.keyCode:!a.which&&void 0!==b&&ta.test(a.type)?1&b?1:2&b?3:4&b?2:0:a.which}},r.event.addProp),r.each({mouseenter:"mouseover",mouseleave:"mouseout",pointerenter:"pointerover",pointerleave:"pointerout"},function(a,b){r.event.special[a]={delegateType:b,bindType:b,handle:function(a){var c,d=this,e=a.relatedTarget,f=a.handleObj;return e&&(e===d||r.contains(d,e))||(a.type=f.origType,c=f.handler.apply(this,arguments),a.type=b),c}}}),r.fn.extend({on:function(a,b,c,d){return ya(this,a,b,c,d)},one:function(a,b,c,d){return ya(this,a,b,c,d,1)},off:function(a,b,c){var d,e;if(a&&a.preventDefault&&a.handleObj)return d=a.handleObj,r(a.delegateTarget).off(d.namespace?d.origType+"."+d.namespace:d.origType,d.selector,d.handler),this;if("object"==typeof a){for(e in a)this.off(e,b,a[e]);return this}return b!==!1&&"function"!=typeof b||(c=b,b=void 0),c===!1&&(c=wa),this.each(function(){r.event.remove(this,a,c,b)})}});var za=/<(?!area|br|col|embed|hr|img|input|link|meta|param)(([a-z][^\/\0>\x20\t\r\n\f]*)[^>]*)\/>/gi,Aa=/<script|<style|<link/i,Ba=/checked\s*(?:[^=]|=\s*.checked.)/i,Ca=/^true\/(.*)/,Da=/^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g;function Ea(a,b){return B(a,"table")&&B(11!==b.nodeType?b:b.firstChild,"tr")?r(">tbody",a)[0]||a:a}function Fa(a){return a.type=(null!==a.getAttribute("type"))+"/"+a.type,a}function Ga(a){var b=Ca.exec(a.type);return b?a.type=b[1]:a.removeAttribute("type"),a}function Ha(a,b){var c,d,e,f,g,h,i,j;if(1===b.nodeType){if(W.hasData(a)&&(f=W.access(a),g=W.set(b,f),j=f.events)){delete g.handle,g.events={};for(e in j)for(c=0,d=j[e].length;c<d;c++)r.event.add(b,e,j[e][c])}X.hasData(a)&&(h=X.access(a),i=r.extend({},h),X.set(b,i))}}function Ia(a,b){var c=b.nodeName.toLowerCase();"input"===c&&ja.test(a.type)?b.checked=a.checked:"input"!==c&&"textarea"!==c||(b.defaultValue=a.defaultValue)}function Ja(a,b,c,d){b=g.apply([],b);var e,f,h,i,j,k,l=0,m=a.length,n=m-1,q=b[0],s=r.isFunction(q);if(s||m>1&&"string"==typeof q&&!o.checkClone&&Ba.test(q))return a.each(function(e){var f=a.eq(e);s&&(b[0]=q.call(this,e,f.html())),Ja(f,b,c,d)});if(m&&(e=qa(b,a[0].ownerDocument,!1,a,d),f=e.firstChild,1===e.childNodes.length&&(e=f),f||d)){for(h=r.map(na(e,"script"),Fa),i=h.length;l<m;l++)j=e,l!==n&&(j=r.clone(j,!0,!0),i&&r.merge(h,na(j,"script"))),c.call(a[l],j,l);if(i)for(k=h[h.length-1].ownerDocument,r.map(h,Ga),l=0;l<i;l++)j=h[l],la.test(j.type||"")&&!W.access(j,"globalEval")&&r.contains(k,j)&&(j.src?r._evalUrl&&r._evalUrl(j.src):p(j.textContent.replace(Da,""),k))}return a}function Ka(a,b,c){for(var d,e=b?r.filter(b,a):a,f=0;null!=(d=e[f]);f++)c||1!==d.nodeType||r.cleanData(na(d)),d.parentNode&&(c&&r.contains(d.ownerDocument,d)&&oa(na(d,"script")),d.parentNode.removeChild(d));return a}r.extend({htmlPrefilter:function(a){return a.replace(za,"<$1></$2>")},clone:function(a,b,c){var d,e,f,g,h=a.cloneNode(!0),i=r.contains(a.ownerDocument,a);if(!(o.noCloneChecked||1!==a.nodeType&&11!==a.nodeType||r.isXMLDoc(a)))for(g=na(h),f=na(a),d=0,e=f.length;d<e;d++)Ia(f[d],g[d]);if(b)if(c)for(f=f||na(a),g=g||na(h),d=0,e=f.length;d<e;d++)Ha(f[d],g[d]);else Ha(a,h);return g=na(h,"script"),g.length>0&&oa(g,!i&&na(a,"script")),h},cleanData:function(a){for(var b,c,d,e=r.event.special,f=0;void 0!==(c=a[f]);f++)if(U(c)){if(b=c[W.expando]){if(b.events)for(d in b.events)e[d]?r.event.remove(c,d):r.removeEvent(c,d,b.handle);c[W.expando]=void 0}c[X.expando]&&(c[X.expando]=void 0)}}}),r.fn.extend({detach:function(a){return Ka(this,a,!0)},remove:function(a){return Ka(this,a)},text:function(a){return T(this,function(a){return void 0===a?r.text(this):this.empty().each(function(){1!==this.nodeType&&11!==this.nodeType&&9!==this.nodeType||(this.textContent=a)})},null,a,arguments.length)},append:function(){return Ja(this,arguments,function(a){if(1===this.nodeType||11===this.nodeType||9===this.nodeType){var b=Ea(this,a);b.appendChild(a)}})},prepend:function(){return Ja(this,arguments,function(a){if(1===this.nodeType||11===this.nodeType||9===this.nodeType){var b=Ea(this,a);b.insertBefore(a,b.firstChild)}})},before:function(){return Ja(this,arguments,function(a){this.parentNode&&this.parentNode.insertBefore(a,this)})},after:function(){return Ja(this,arguments,function(a){this.parentNode&&this.parentNode.insertBefore(a,this.nextSibling)})},empty:function(){for(var a,b=0;null!=(a=this[b]);b++)1===a.nodeType&&(r.cleanData(na(a,!1)),a.textContent="");return this},clone:function(a,b){return a=null!=a&&a,b=null==b?a:b,this.map(function(){return r.clone(this,a,b)})},html:function(a){return T(this,function(a){var b=this[0]||{},c=0,d=this.length;if(void 0===a&&1===b.nodeType)return b.innerHTML;if("string"==typeof a&&!Aa.test(a)&&!ma[(ka.exec(a)||["",""])[1].toLowerCase()]){a=r.htmlPrefilter(a);try{for(;c<d;c++)b=this[c]||{},1===b.nodeType&&(r.cleanData(na(b,!1)),b.innerHTML=a);b=0}catch(e){}}b&&this.empty().append(a)},null,a,arguments.length)},replaceWith:function(){var a=[];return Ja(this,arguments,function(b){var c=this.parentNode;r.inArray(this,a)<0&&(r.cleanData(na(this)),c&&c.replaceChild(b,this))},a)}}),r.each({appendTo:"append",prependTo:"prepend",insertBefore:"before",insertAfter:"after",replaceAll:"replaceWith"},function(a,b){r.fn[a]=function(a){for(var c,d=[],e=r(a),f=e.length-1,g=0;g<=f;g++)c=g===f?this:this.clone(!0),r(e[g])[b](c),h.apply(d,c.get());return this.pushStack(d)}});var La=/^margin/,Ma=new RegExp("^("+aa+")(?!px)[a-z%]+$","i"),Na=function(b){var c=b.ownerDocument.defaultView;return c&&c.opener||(c=a),c.getComputedStyle(b)};!function(){function b(){if(i){i.style.cssText="box-sizing:border-box;position:relative;display:block;margin:auto;border:1px;padding:1px;top:1%;width:50%",i.innerHTML="",ra.appendChild(h);var b=a.getComputedStyle(i);c="1%"!==b.top,g="2px"===b.marginLeft,e="4px"===b.width,i.style.marginRight="50%",f="4px"===b.marginRight,ra.removeChild(h),i=null}}var c,e,f,g,h=d.createElement("div"),i=d.createElement("div");i.style&&(i.style.backgroundClip="content-box",i.cloneNode(!0).style.backgroundClip="",o.clearCloneStyle="content-box"===i.style.backgroundClip,h.style.cssText="border:0;width:8px;height:0;top:0;left:-9999px;padding:0;margin-top:1px;position:absolute",h.appendChild(i),r.extend(o,{pixelPosition:function(){return b(),c},boxSizingReliable:function(){return b(),e},pixelMarginRight:function(){return b(),f},reliableMarginLeft:function(){return b(),g}}))}();function Oa(a,b,c){var d,e,f,g,h=a.style;return c=c||Na(a),c&&(g=c.getPropertyValue(b)||c[b],""!==g||r.contains(a.ownerDocument,a)||(g=r.style(a,b)),!o.pixelMarginRight()&&Ma.test(g)&&La.test(b)&&(d=h.width,e=h.minWidth,f=h.maxWidth,h.minWidth=h.maxWidth=h.width=g,g=c.width,h.width=d,h.minWidth=e,h.maxWidth=f)),void 0!==g?g+"":g}function Pa(a,b){return{get:function(){return a()?void delete this.get:(this.get=b).apply(this,arguments)}}}var Qa=/^(none|table(?!-c[ea]).+)/,Ra=/^--/,Sa={position:"absolute",visibility:"hidden",display:"block"},Ta={letterSpacing:"0",fontWeight:"400"},Ua=["Webkit","Moz","ms"],Va=d.createElement("div").style;function Wa(a){if(a in Va)return a;var b=a[0].toUpperCase()+a.slice(1),c=Ua.length;while(c--)if(a=Ua[c]+b,a in Va)return a}function Xa(a){var b=r.cssProps[a];return b||(b=r.cssProps[a]=Wa(a)||a),b}function Ya(a,b,c){var d=ba.exec(b);return d?Math.max(0,d[2]-(c||0))+(d[3]||"px"):b}function Za(a,b,c,d,e){var f,g=0;for(f=c===(d?"border":"content")?4:"width"===b?1:0;f<4;f+=2)"margin"===c&&(g+=r.css(a,c+ca[f],!0,e)),d?("content"===c&&(g-=r.css(a,"padding"+ca[f],!0,e)),"margin"!==c&&(g-=r.css(a,"border"+ca[f]+"Width",!0,e))):(g+=r.css(a,"padding"+ca[f],!0,e),"padding"!==c&&(g+=r.css(a,"border"+ca[f]+"Width",!0,e)));return g}function $a(a,b,c){var d,e=Na(a),f=Oa(a,b,e),g="border-box"===r.css(a,"boxSizing",!1,e);return Ma.test(f)?f:(d=g&&(o.boxSizingReliable()||f===a.style[b]),"auto"===f&&(f=a["offset"+b[0].toUpperCase()+b.slice(1)]),f=parseFloat(f)||0,f+Za(a,b,c||(g?"border":"content"),d,e)+"px")}r.extend({cssHooks:{opacity:{get:function(a,b){if(b){var c=Oa(a,"opacity");return""===c?"1":c}}}},cssNumber:{animationIterationCount:!0,columnCount:!0,fillOpacity:!0,flexGrow:!0,flexShrink:!0,fontWeight:!0,lineHeight:!0,opacity:!0,order:!0,orphans:!0,widows:!0,zIndex:!0,zoom:!0},cssProps:{"float":"cssFloat"},style:function(a,b,c,d){if(a&&3!==a.nodeType&&8!==a.nodeType&&a.style){var e,f,g,h=r.camelCase(b),i=Ra.test(b),j=a.style;return i||(b=Xa(h)),g=r.cssHooks[b]||r.cssHooks[h],void 0===c?g&&"get"in g&&void 0!==(e=g.get(a,!1,d))?e:j[b]:(f=typeof c,"string"===f&&(e=ba.exec(c))&&e[1]&&(c=fa(a,b,e),f="number"),null!=c&&c===c&&("number"===f&&(c+=e&&e[3]||(r.cssNumber[h]?"":"px")),o.clearCloneStyle||""!==c||0!==b.indexOf("background")||(j[b]="inherit"),g&&"set"in g&&void 0===(c=g.set(a,c,d))||(i?j.setProperty(b,c):j[b]=c)),void 0)}},css:function(a,b,c,d){var e,f,g,h=r.camelCase(b),i=Ra.test(b);return i||(b=Xa(h)),g=r.cssHooks[b]||r.cssHooks[h],g&&"get"in g&&(e=g.get(a,!0,c)),void 0===e&&(e=Oa(a,b,d)),"normal"===e&&b in Ta&&(e=Ta[b]),""===c||c?(f=parseFloat(e),c===!0||isFinite(f)?f||0:e):e}}),r.each(["height","width"],function(a,b){r.cssHooks[b]={get:function(a,c,d){if(c)return!Qa.test(r.css(a,"display"))||a.getClientRects().length&&a.getBoundingClientRect().width?$a(a,b,d):ea(a,Sa,function(){return $a(a,b,d)})},set:function(a,c,d){var e,f=d&&Na(a),g=d&&Za(a,b,d,"border-box"===r.css(a,"boxSizing",!1,f),f);return g&&(e=ba.exec(c))&&"px"!==(e[3]||"px")&&(a.style[b]=c,c=r.css(a,b)),Ya(a,c,g)}}}),r.cssHooks.marginLeft=Pa(o.reliableMarginLeft,function(a,b){if(b)return(parseFloat(Oa(a,"marginLeft"))||a.getBoundingClientRect().left-ea(a,{marginLeft:0},function(){return a.getBoundingClientRect().left}))+"px"}),r.each({margin:"",padding:"",border:"Width"},function(a,b){r.cssHooks[a+b]={expand:function(c){for(var d=0,e={},f="string"==typeof c?c.split(" "):[c];d<4;d++)e[a+ca[d]+b]=f[d]||f[d-2]||f[0];return e}},La.test(a)||(r.cssHooks[a+b].set=Ya)}),r.fn.extend({css:function(a,b){return T(this,function(a,b,c){var d,e,f={},g=0;if(Array.isArray(b)){for(d=Na(a),e=b.length;g<e;g++)f[b[g]]=r.css(a,b[g],!1,d);return f}return void 0!==c?r.style(a,b,c):r.css(a,b)},a,b,arguments.length>1)}});function _a(a,b,c,d,e){return new _a.prototype.init(a,b,c,d,e)}r.Tween=_a,_a.prototype={constructor:_a,init:function(a,b,c,d,e,f){this.elem=a,this.prop=c,this.easing=e||r.easing._default,this.options=b,this.start=this.now=this.cur(),this.end=d,this.unit=f||(r.cssNumber[c]?"":"px")},cur:function(){var a=_a.propHooks[this.prop];return a&&a.get?a.get(this):_a.propHooks._default.get(this)},run:function(a){var b,c=_a.propHooks[this.prop];return this.options.duration?this.pos=b=r.easing[this.easing](a,this.options.duration*a,0,1,this.options.duration):this.pos=b=a,this.now=(this.end-this.start)*b+this.start,this.options.step&&this.options.step.call(this.elem,this.now,this),c&&c.set?c.set(this):_a.propHooks._default.set(this),this}},_a.prototype.init.prototype=_a.prototype,_a.propHooks={_default:{get:function(a){var b;return 1!==a.elem.nodeType||null!=a.elem[a.prop]&&null==a.elem.style[a.prop]?a.elem[a.prop]:(b=r.css(a.elem,a.prop,""),b&&"auto"!==b?b:0)},set:function(a){r.fx.step[a.prop]?r.fx.step[a.prop](a):1!==a.elem.nodeType||null==a.elem.style[r.cssProps[a.prop]]&&!r.cssHooks[a.prop]?a.elem[a.prop]=a.now:r.style(a.elem,a.prop,a.now+a.unit)}}},_a.propHooks.scrollTop=_a.propHooks.scrollLeft={set:function(a){a.elem.nodeType&&a.elem.parentNode&&(a.elem[a.prop]=a.now)}},r.easing={linear:function(a){return a},swing:function(a){return.5-Math.cos(a*Math.PI)/2},_default:"swing"},r.fx=_a.prototype.init,r.fx.step={};var ab,bb,cb=/^(?:toggle|show|hide)$/,db=/queueHooks$/;function eb(){bb&&(d.hidden===!1&&a.requestAnimationFrame?a.requestAnimationFrame(eb):a.setTimeout(eb,r.fx.interval),r.fx.tick())}function fb(){return a.setTimeout(function(){ab=void 0}),ab=r.now()}function gb(a,b){var c,d=0,e={height:a};for(b=b?1:0;d<4;d+=2-b)c=ca[d],e["margin"+c]=e["padding"+c]=a;return b&&(e.opacity=e.width=a),e}function hb(a,b,c){for(var d,e=(kb.tweeners[b]||[]).concat(kb.tweeners["*"]),f=0,g=e.length;f<g;f++)if(d=e[f].call(c,b,a))return d}function ib(a,b,c){var d,e,f,g,h,i,j,k,l="width"in b||"height"in b,m=this,n={},o=a.style,p=a.nodeType&&da(a),q=W.get(a,"fxshow");c.queue||(g=r._queueHooks(a,"fx"),null==g.unqueued&&(g.unqueued=0,h=g.empty.fire,g.empty.fire=function(){g.unqueued||h()}),g.unqueued++,m.always(function(){m.always(function(){g.unqueued--,r.queue(a,"fx").length||g.empty.fire()})}));for(d in b)if(e=b[d],cb.test(e)){if(delete b[d],f=f||"toggle"===e,e===(p?"hide":"show")){if("show"!==e||!q||void 0===q[d])continue;p=!0}n[d]=q&&q[d]||r.style(a,d)}if(i=!r.isEmptyObject(b),i||!r.isEmptyObject(n)){l&&1===a.nodeType&&(c.overflow=[o.overflow,o.overflowX,o.overflowY],j=q&&q.display,null==j&&(j=W.get(a,"display")),k=r.css(a,"display"),"none"===k&&(j?k=j:(ia([a],!0),j=a.style.display||j,k=r.css(a,"display"),ia([a]))),("inline"===k||"inline-block"===k&&null!=j)&&"none"===r.css(a,"float")&&(i||(m.done(function(){o.display=j}),null==j&&(k=o.display,j="none"===k?"":k)),o.display="inline-block")),c.overflow&&(o.overflow="hidden",m.always(function(){o.overflow=c.overflow[0],o.overflowX=c.overflow[1],o.overflowY=c.overflow[2]})),i=!1;for(d in n)i||(q?"hidden"in q&&(p=q.hidden):q=W.access(a,"fxshow",{display:j}),f&&(q.hidden=!p),p&&ia([a],!0),m.done(function(){p||ia([a]),W.remove(a,"fxshow");for(d in n)r.style(a,d,n[d])})),i=hb(p?q[d]:0,d,m),d in q||(q[d]=i.start,p&&(i.end=i.start,i.start=0))}}function jb(a,b){var c,d,e,f,g;for(c in a)if(d=r.camelCase(c),e=b[d],f=a[c],Array.isArray(f)&&(e=f[1],f=a[c]=f[0]),c!==d&&(a[d]=f,delete a[c]),g=r.cssHooks[d],g&&"expand"in g){f=g.expand(f),delete a[d];for(c in f)c in a||(a[c]=f[c],b[c]=e)}else b[d]=e}function kb(a,b,c){var d,e,f=0,g=kb.prefilters.length,h=r.Deferred().always(function(){delete i.elem}),i=function(){if(e)return!1;for(var b=ab||fb(),c=Math.max(0,j.startTime+j.duration-b),d=c/j.duration||0,f=1-d,g=0,i=j.tweens.length;g<i;g++)j.tweens[g].run(f);return h.notifyWith(a,[j,f,c]),f<1&&i?c:(i||h.notifyWith(a,[j,1,0]),h.resolveWith(a,[j]),!1)},j=h.promise({elem:a,props:r.extend({},b),opts:r.extend(!0,{specialEasing:{},easing:r.easing._default},c),originalProperties:b,originalOptions:c,startTime:ab||fb(),duration:c.duration,tweens:[],createTween:function(b,c){var d=r.Tween(a,j.opts,b,c,j.opts.specialEasing[b]||j.opts.easing);return j.tweens.push(d),d},stop:function(b){var c=0,d=b?j.tweens.length:0;if(e)return this;for(e=!0;c<d;c++)j.tweens[c].run(1);return b?(h.notifyWith(a,[j,1,0]),h.resolveWith(a,[j,b])):h.rejectWith(a,[j,b]),this}}),k=j.props;for(jb(k,j.opts.specialEasing);f<g;f++)if(d=kb.prefilters[f].call(j,a,k,j.opts))return r.isFunction(d.stop)&&(r._queueHooks(j.elem,j.opts.queue).stop=r.proxy(d.stop,d)),d;return r.map(k,hb,j),r.isFunction(j.opts.start)&&j.opts.start.call(a,j),j.progress(j.opts.progress).done(j.opts.done,j.opts.complete).fail(j.opts.fail).always(j.opts.always),r.fx.timer(r.extend(i,{elem:a,anim:j,queue:j.opts.queue})),j}r.Animation=r.extend(kb,{tweeners:{"*":[function(a,b){var c=this.createTween(a,b);return fa(c.elem,a,ba.exec(b),c),c}]},tweener:function(a,b){r.isFunction(a)?(b=a,a=["*"]):a=a.match(L);for(var c,d=0,e=a.length;d<e;d++)c=a[d],kb.tweeners[c]=kb.tweeners[c]||[],kb.tweeners[c].unshift(b)},prefilters:[ib],prefilter:function(a,b){b?kb.prefilters.unshift(a):kb.prefilters.push(a)}}),r.speed=function(a,b,c){var d=a&&"object"==typeof a?r.extend({},a):{complete:c||!c&&b||r.isFunction(a)&&a,duration:a,easing:c&&b||b&&!r.isFunction(b)&&b};return r.fx.off?d.duration=0:"number"!=typeof d.duration&&(d.duration in r.fx.speeds?d.duration=r.fx.speeds[d.duration]:d.duration=r.fx.speeds._default),null!=d.queue&&d.queue!==!0||(d.queue="fx"),d.old=d.complete,d.complete=function(){r.isFunction(d.old)&&d.old.call(this),d.queue&&r.dequeue(this,d.queue)},d},r.fn.extend({fadeTo:function(a,b,c,d){return this.filter(da).css("opacity",0).show().end().animate({opacity:b},a,c,d)},animate:function(a,b,c,d){var e=r.isEmptyObject(a),f=r.speed(b,c,d),g=function(){var b=kb(this,r.extend({},a),f);(e||W.get(this,"finish"))&&b.stop(!0)};return g.finish=g,e||f.queue===!1?this.each(g):this.queue(f.queue,g)},stop:function(a,b,c){var d=function(a){var b=a.stop;delete a.stop,b(c)};return"string"!=typeof a&&(c=b,b=a,a=void 0),b&&a!==!1&&this.queue(a||"fx",[]),this.each(function(){var b=!0,e=null!=a&&a+"queueHooks",f=r.timers,g=W.get(this);if(e)g[e]&&g[e].stop&&d(g[e]);else for(e in g)g[e]&&g[e].stop&&db.test(e)&&d(g[e]);for(e=f.length;e--;)f[e].elem!==this||null!=a&&f[e].queue!==a||(f[e].anim.stop(c),b=!1,f.splice(e,1));!b&&c||r.dequeue(this,a)})},finish:function(a){return a!==!1&&(a=a||"fx"),this.each(function(){var b,c=W.get(this),d=c[a+"queue"],e=c[a+"queueHooks"],f=r.timers,g=d?d.length:0;for(c.finish=!0,r.queue(this,a,[]),e&&e.stop&&e.stop.call(this,!0),b=f.length;b--;)f[b].elem===this&&f[b].queue===a&&(f[b].anim.stop(!0),f.splice(b,1));for(b=0;b<g;b++)d[b]&&d[b].finish&&d[b].finish.call(this);delete c.finish})}}),r.each(["toggle","show","hide"],function(a,b){var c=r.fn[b];r.fn[b]=function(a,d,e){return null==a||"boolean"==typeof a?c.apply(this,arguments):this.animate(gb(b,!0),a,d,e)}}),r.each({slideDown:gb("show"),slideUp:gb("hide"),slideToggle:gb("toggle"),fadeIn:{opacity:"show"},fadeOut:{opacity:"hide"},fadeToggle:{opacity:"toggle"}},function(a,b){r.fn[a]=function(a,c,d){return this.animate(b,a,c,d)}}),r.timers=[],r.fx.tick=function(){var a,b=0,c=r.timers;for(ab=r.now();b<c.length;b++)a=c[b],a()||c[b]!==a||c.splice(b--,1);c.length||r.fx.stop(),ab=void 0},r.fx.timer=function(a){r.timers.push(a),r.fx.start()},r.fx.interval=13,r.fx.start=function(){bb||(bb=!0,eb())},r.fx.stop=function(){bb=null},r.fx.speeds={slow:600,fast:200,_default:400},r.fn.delay=function(b,c){return b=r.fx?r.fx.speeds[b]||b:b,c=c||"fx",this.queue(c,function(c,d){var e=a.setTimeout(c,b);d.stop=function(){a.clearTimeout(e)}})},function(){var a=d.createElement("input"),b=d.createElement("select"),c=b.appendChild(d.createElement("option"));a.type="checkbox",o.checkOn=""!==a.value,o.optSelected=c.selected,a=d.createElement("input"),a.value="t",a.type="radio",o.radioValue="t"===a.value}();var lb,mb=r.expr.attrHandle;r.fn.extend({attr:function(a,b){return T(this,r.attr,a,b,arguments.length>1)},removeAttr:function(a){return this.each(function(){r.removeAttr(this,a)})}}),r.extend({attr:function(a,b,c){var d,e,f=a.nodeType;if(3!==f&&8!==f&&2!==f)return"undefined"==typeof a.getAttribute?r.prop(a,b,c):(1===f&&r.isXMLDoc(a)||(e=r.attrHooks[b.toLowerCase()]||(r.expr.match.bool.test(b)?lb:void 0)),void 0!==c?null===c?void r.removeAttr(a,b):e&&"set"in e&&void 0!==(d=e.set(a,c,b))?d:(a.setAttribute(b,c+""),c):e&&"get"in e&&null!==(d=e.get(a,b))?d:(d=r.find.attr(a,b),
null==d?void 0:d))},attrHooks:{type:{set:function(a,b){if(!o.radioValue&&"radio"===b&&B(a,"input")){var c=a.value;return a.setAttribute("type",b),c&&(a.value=c),b}}}},removeAttr:function(a,b){var c,d=0,e=b&&b.match(L);if(e&&1===a.nodeType)while(c=e[d++])a.removeAttribute(c)}}),lb={set:function(a,b,c){return b===!1?r.removeAttr(a,c):a.setAttribute(c,c),c}},r.each(r.expr.match.bool.source.match(/\w+/g),function(a,b){var c=mb[b]||r.find.attr;mb[b]=function(a,b,d){var e,f,g=b.toLowerCase();return d||(f=mb[g],mb[g]=e,e=null!=c(a,b,d)?g:null,mb[g]=f),e}});var nb=/^(?:input|select|textarea|button)$/i,ob=/^(?:a|area)$/i;r.fn.extend({prop:function(a,b){return T(this,r.prop,a,b,arguments.length>1)},removeProp:function(a){return this.each(function(){delete this[r.propFix[a]||a]})}}),r.extend({prop:function(a,b,c){var d,e,f=a.nodeType;if(3!==f&&8!==f&&2!==f)return 1===f&&r.isXMLDoc(a)||(b=r.propFix[b]||b,e=r.propHooks[b]),void 0!==c?e&&"set"in e&&void 0!==(d=e.set(a,c,b))?d:a[b]=c:e&&"get"in e&&null!==(d=e.get(a,b))?d:a[b]},propHooks:{tabIndex:{get:function(a){var b=r.find.attr(a,"tabindex");return b?parseInt(b,10):nb.test(a.nodeName)||ob.test(a.nodeName)&&a.href?0:-1}}},propFix:{"for":"htmlFor","class":"className"}}),o.optSelected||(r.propHooks.selected={get:function(a){var b=a.parentNode;return b&&b.parentNode&&b.parentNode.selectedIndex,null},set:function(a){var b=a.parentNode;b&&(b.selectedIndex,b.parentNode&&b.parentNode.selectedIndex)}}),r.each(["tabIndex","readOnly","maxLength","cellSpacing","cellPadding","rowSpan","colSpan","useMap","frameBorder","contentEditable"],function(){r.propFix[this.toLowerCase()]=this});function pb(a){var b=a.match(L)||[];return b.join(" ")}function qb(a){return a.getAttribute&&a.getAttribute("class")||""}r.fn.extend({addClass:function(a){var b,c,d,e,f,g,h,i=0;if(r.isFunction(a))return this.each(function(b){r(this).addClass(a.call(this,b,qb(this)))});if("string"==typeof a&&a){b=a.match(L)||[];while(c=this[i++])if(e=qb(c),d=1===c.nodeType&&" "+pb(e)+" "){g=0;while(f=b[g++])d.indexOf(" "+f+" ")<0&&(d+=f+" ");h=pb(d),e!==h&&c.setAttribute("class",h)}}return this},removeClass:function(a){var b,c,d,e,f,g,h,i=0;if(r.isFunction(a))return this.each(function(b){r(this).removeClass(a.call(this,b,qb(this)))});if(!arguments.length)return this.attr("class","");if("string"==typeof a&&a){b=a.match(L)||[];while(c=this[i++])if(e=qb(c),d=1===c.nodeType&&" "+pb(e)+" "){g=0;while(f=b[g++])while(d.indexOf(" "+f+" ")>-1)d=d.replace(" "+f+" "," ");h=pb(d),e!==h&&c.setAttribute("class",h)}}return this},toggleClass:function(a,b){var c=typeof a;return"boolean"==typeof b&&"string"===c?b?this.addClass(a):this.removeClass(a):r.isFunction(a)?this.each(function(c){r(this).toggleClass(a.call(this,c,qb(this),b),b)}):this.each(function(){var b,d,e,f;if("string"===c){d=0,e=r(this),f=a.match(L)||[];while(b=f[d++])e.hasClass(b)?e.removeClass(b):e.addClass(b)}else void 0!==a&&"boolean"!==c||(b=qb(this),b&&W.set(this,"__className__",b),this.setAttribute&&this.setAttribute("class",b||a===!1?"":W.get(this,"__className__")||""))})},hasClass:function(a){var b,c,d=0;b=" "+a+" ";while(c=this[d++])if(1===c.nodeType&&(" "+pb(qb(c))+" ").indexOf(b)>-1)return!0;return!1}});var rb=/\r/g;r.fn.extend({val:function(a){var b,c,d,e=this[0];{if(arguments.length)return d=r.isFunction(a),this.each(function(c){var e;1===this.nodeType&&(e=d?a.call(this,c,r(this).val()):a,null==e?e="":"number"==typeof e?e+="":Array.isArray(e)&&(e=r.map(e,function(a){return null==a?"":a+""})),b=r.valHooks[this.type]||r.valHooks[this.nodeName.toLowerCase()],b&&"set"in b&&void 0!==b.set(this,e,"value")||(this.value=e))});if(e)return b=r.valHooks[e.type]||r.valHooks[e.nodeName.toLowerCase()],b&&"get"in b&&void 0!==(c=b.get(e,"value"))?c:(c=e.value,"string"==typeof c?c.replace(rb,""):null==c?"":c)}}}),r.extend({valHooks:{option:{get:function(a){var b=r.find.attr(a,"value");return null!=b?b:pb(r.text(a))}},select:{get:function(a){var b,c,d,e=a.options,f=a.selectedIndex,g="select-one"===a.type,h=g?null:[],i=g?f+1:e.length;for(d=f<0?i:g?f:0;d<i;d++)if(c=e[d],(c.selected||d===f)&&!c.disabled&&(!c.parentNode.disabled||!B(c.parentNode,"optgroup"))){if(b=r(c).val(),g)return b;h.push(b)}return h},set:function(a,b){var c,d,e=a.options,f=r.makeArray(b),g=e.length;while(g--)d=e[g],(d.selected=r.inArray(r.valHooks.option.get(d),f)>-1)&&(c=!0);return c||(a.selectedIndex=-1),f}}}}),r.each(["radio","checkbox"],function(){r.valHooks[this]={set:function(a,b){if(Array.isArray(b))return a.checked=r.inArray(r(a).val(),b)>-1}},o.checkOn||(r.valHooks[this].get=function(a){return null===a.getAttribute("value")?"on":a.value})});var sb=/^(?:focusinfocus|focusoutblur)$/;r.extend(r.event,{trigger:function(b,c,e,f){var g,h,i,j,k,m,n,o=[e||d],p=l.call(b,"type")?b.type:b,q=l.call(b,"namespace")?b.namespace.split("."):[];if(h=i=e=e||d,3!==e.nodeType&&8!==e.nodeType&&!sb.test(p+r.event.triggered)&&(p.indexOf(".")>-1&&(q=p.split("."),p=q.shift(),q.sort()),k=p.indexOf(":")<0&&"on"+p,b=b[r.expando]?b:new r.Event(p,"object"==typeof b&&b),b.isTrigger=f?2:3,b.namespace=q.join("."),b.rnamespace=b.namespace?new RegExp("(^|\\.)"+q.join("\\.(?:.*\\.|)")+"(\\.|$)"):null,b.result=void 0,b.target||(b.target=e),c=null==c?[b]:r.makeArray(c,[b]),n=r.event.special[p]||{},f||!n.trigger||n.trigger.apply(e,c)!==!1)){if(!f&&!n.noBubble&&!r.isWindow(e)){for(j=n.delegateType||p,sb.test(j+p)||(h=h.parentNode);h;h=h.parentNode)o.push(h),i=h;i===(e.ownerDocument||d)&&o.push(i.defaultView||i.parentWindow||a)}g=0;while((h=o[g++])&&!b.isPropagationStopped())b.type=g>1?j:n.bindType||p,m=(W.get(h,"events")||{})[b.type]&&W.get(h,"handle"),m&&m.apply(h,c),m=k&&h[k],m&&m.apply&&U(h)&&(b.result=m.apply(h,c),b.result===!1&&b.preventDefault());return b.type=p,f||b.isDefaultPrevented()||n._default&&n._default.apply(o.pop(),c)!==!1||!U(e)||k&&r.isFunction(e[p])&&!r.isWindow(e)&&(i=e[k],i&&(e[k]=null),r.event.triggered=p,e[p](),r.event.triggered=void 0,i&&(e[k]=i)),b.result}},simulate:function(a,b,c){var d=r.extend(new r.Event,c,{type:a,isSimulated:!0});r.event.trigger(d,null,b)}}),r.fn.extend({trigger:function(a,b){return this.each(function(){r.event.trigger(a,b,this)})},triggerHandler:function(a,b){var c=this[0];if(c)return r.event.trigger(a,b,c,!0)}}),r.each("blur focus focusin focusout resize scroll click dblclick mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave change select submit keydown keypress keyup contextmenu".split(" "),function(a,b){r.fn[b]=function(a,c){return arguments.length>0?this.on(b,null,a,c):this.trigger(b)}}),r.fn.extend({hover:function(a,b){return this.mouseenter(a).mouseleave(b||a)}}),o.focusin="onfocusin"in a,o.focusin||r.each({focus:"focusin",blur:"focusout"},function(a,b){var c=function(a){r.event.simulate(b,a.target,r.event.fix(a))};r.event.special[b]={setup:function(){var d=this.ownerDocument||this,e=W.access(d,b);e||d.addEventListener(a,c,!0),W.access(d,b,(e||0)+1)},teardown:function(){var d=this.ownerDocument||this,e=W.access(d,b)-1;e?W.access(d,b,e):(d.removeEventListener(a,c,!0),W.remove(d,b))}}});var tb=a.location,ub=r.now(),vb=/\?/;r.parseXML=function(b){var c;if(!b||"string"!=typeof b)return null;try{c=(new a.DOMParser).parseFromString(b,"text/xml")}catch(d){c=void 0}return c&&!c.getElementsByTagName("parsererror").length||r.error("Invalid XML: "+b),c};var wb=/\[\]$/,xb=/\r?\n/g,yb=/^(?:submit|button|image|reset|file)$/i,zb=/^(?:input|select|textarea|keygen)/i;function Ab(a,b,c,d){var e;if(Array.isArray(b))r.each(b,function(b,e){c||wb.test(a)?d(a,e):Ab(a+"["+("object"==typeof e&&null!=e?b:"")+"]",e,c,d)});else if(c||"object"!==r.type(b))d(a,b);else for(e in b)Ab(a+"["+e+"]",b[e],c,d)}r.param=function(a,b){var c,d=[],e=function(a,b){var c=r.isFunction(b)?b():b;d[d.length]=encodeURIComponent(a)+"="+encodeURIComponent(null==c?"":c)};if(Array.isArray(a)||a.jquery&&!r.isPlainObject(a))r.each(a,function(){e(this.name,this.value)});else for(c in a)Ab(c,a[c],b,e);return d.join("&")},r.fn.extend({serialize:function(){return r.param(this.serializeArray())},serializeArray:function(){return this.map(function(){var a=r.prop(this,"elements");return a?r.makeArray(a):this}).filter(function(){var a=this.type;return this.name&&!r(this).is(":disabled")&&zb.test(this.nodeName)&&!yb.test(a)&&(this.checked||!ja.test(a))}).map(function(a,b){var c=r(this).val();return null==c?null:Array.isArray(c)?r.map(c,function(a){return{name:b.name,value:a.replace(xb,"\r\n")}}):{name:b.name,value:c.replace(xb,"\r\n")}}).get()}});var Bb=/%20/g,Cb=/#.*$/,Db=/([?&])_=[^&]*/,Eb=/^(.*?):[ \t]*([^\r\n]*)$/gm,Fb=/^(?:about|app|app-storage|.+-extension|file|res|widget):$/,Gb=/^(?:GET|HEAD)$/,Hb=/^\/\//,Ib={},Jb={},Kb="*/".concat("*"),Lb=d.createElement("a");Lb.href=tb.href;function Mb(a){return function(b,c){"string"!=typeof b&&(c=b,b="*");var d,e=0,f=b.toLowerCase().match(L)||[];if(r.isFunction(c))while(d=f[e++])"+"===d[0]?(d=d.slice(1)||"*",(a[d]=a[d]||[]).unshift(c)):(a[d]=a[d]||[]).push(c)}}function Nb(a,b,c,d){var e={},f=a===Jb;function g(h){var i;return e[h]=!0,r.each(a[h]||[],function(a,h){var j=h(b,c,d);return"string"!=typeof j||f||e[j]?f?!(i=j):void 0:(b.dataTypes.unshift(j),g(j),!1)}),i}return g(b.dataTypes[0])||!e["*"]&&g("*")}function Ob(a,b){var c,d,e=r.ajaxSettings.flatOptions||{};for(c in b)void 0!==b[c]&&((e[c]?a:d||(d={}))[c]=b[c]);return d&&r.extend(!0,a,d),a}function Pb(a,b,c){var d,e,f,g,h=a.contents,i=a.dataTypes;while("*"===i[0])i.shift(),void 0===d&&(d=a.mimeType||b.getResponseHeader("Content-Type"));if(d)for(e in h)if(h[e]&&h[e].test(d)){i.unshift(e);break}if(i[0]in c)f=i[0];else{for(e in c){if(!i[0]||a.converters[e+" "+i[0]]){f=e;break}g||(g=e)}f=f||g}if(f)return f!==i[0]&&i.unshift(f),c[f]}function Qb(a,b,c,d){var e,f,g,h,i,j={},k=a.dataTypes.slice();if(k[1])for(g in a.converters)j[g.toLowerCase()]=a.converters[g];f=k.shift();while(f)if(a.responseFields[f]&&(c[a.responseFields[f]]=b),!i&&d&&a.dataFilter&&(b=a.dataFilter(b,a.dataType)),i=f,f=k.shift())if("*"===f)f=i;else if("*"!==i&&i!==f){if(g=j[i+" "+f]||j["* "+f],!g)for(e in j)if(h=e.split(" "),h[1]===f&&(g=j[i+" "+h[0]]||j["* "+h[0]])){g===!0?g=j[e]:j[e]!==!0&&(f=h[0],k.unshift(h[1]));break}if(g!==!0)if(g&&a["throws"])b=g(b);else try{b=g(b)}catch(l){return{state:"parsererror",error:g?l:"No conversion from "+i+" to "+f}}}return{state:"success",data:b}}r.extend({active:0,lastModified:{},etag:{},ajaxSettings:{url:tb.href,type:"GET",isLocal:Fb.test(tb.protocol),global:!0,processData:!0,async:!0,contentType:"application/x-www-form-urlencoded; charset=UTF-8",accepts:{"*":Kb,text:"text/plain",html:"text/html",xml:"application/xml, text/xml",json:"application/json, text/javascript"},contents:{xml:/\bxml\b/,html:/\bhtml/,json:/\bjson\b/},responseFields:{xml:"responseXML",text:"responseText",json:"responseJSON"},converters:{"* text":String,"text html":!0,"text json":JSON.parse,"text xml":r.parseXML},flatOptions:{url:!0,context:!0}},ajaxSetup:function(a,b){return b?Ob(Ob(a,r.ajaxSettings),b):Ob(r.ajaxSettings,a)},ajaxPrefilter:Mb(Ib),ajaxTransport:Mb(Jb),ajax:function(b,c){"object"==typeof b&&(c=b,b=void 0),c=c||{};var e,f,g,h,i,j,k,l,m,n,o=r.ajaxSetup({},c),p=o.context||o,q=o.context&&(p.nodeType||p.jquery)?r(p):r.event,s=r.Deferred(),t=r.Callbacks("once memory"),u=o.statusCode||{},v={},w={},x="canceled",y={readyState:0,getResponseHeader:function(a){var b;if(k){if(!h){h={};while(b=Eb.exec(g))h[b[1].toLowerCase()]=b[2]}b=h[a.toLowerCase()]}return null==b?null:b},getAllResponseHeaders:function(){return k?g:null},setRequestHeader:function(a,b){return null==k&&(a=w[a.toLowerCase()]=w[a.toLowerCase()]||a,v[a]=b),this},overrideMimeType:function(a){return null==k&&(o.mimeType=a),this},statusCode:function(a){var b;if(a)if(k)y.always(a[y.status]);else for(b in a)u[b]=[u[b],a[b]];return this},abort:function(a){var b=a||x;return e&&e.abort(b),A(0,b),this}};if(s.promise(y),o.url=((b||o.url||tb.href)+"").replace(Hb,tb.protocol+"//"),o.type=c.method||c.type||o.method||o.type,o.dataTypes=(o.dataType||"*").toLowerCase().match(L)||[""],null==o.crossDomain){j=d.createElement("a");try{j.href=o.url,j.href=j.href,o.crossDomain=Lb.protocol+"//"+Lb.host!=j.protocol+"//"+j.host}catch(z){o.crossDomain=!0}}if(o.data&&o.processData&&"string"!=typeof o.data&&(o.data=r.param(o.data,o.traditional)),Nb(Ib,o,c,y),k)return y;l=r.event&&o.global,l&&0===r.active++&&r.event.trigger("ajaxStart"),o.type=o.type.toUpperCase(),o.hasContent=!Gb.test(o.type),f=o.url.replace(Cb,""),o.hasContent?o.data&&o.processData&&0===(o.contentType||"").indexOf("application/x-www-form-urlencoded")&&(o.data=o.data.replace(Bb,"+")):(n=o.url.slice(f.length),o.data&&(f+=(vb.test(f)?"&":"?")+o.data,delete o.data),o.cache===!1&&(f=f.replace(Db,"$1"),n=(vb.test(f)?"&":"?")+"_="+ub++ +n),o.url=f+n),o.ifModified&&(r.lastModified[f]&&y.setRequestHeader("If-Modified-Since",r.lastModified[f]),r.etag[f]&&y.setRequestHeader("If-None-Match",r.etag[f])),(o.data&&o.hasContent&&o.contentType!==!1||c.contentType)&&y.setRequestHeader("Content-Type",o.contentType),y.setRequestHeader("Accept",o.dataTypes[0]&&o.accepts[o.dataTypes[0]]?o.accepts[o.dataTypes[0]]+("*"!==o.dataTypes[0]?", "+Kb+"; q=0.01":""):o.accepts["*"]);for(m in o.headers)y.setRequestHeader(m,o.headers[m]);if(o.beforeSend&&(o.beforeSend.call(p,y,o)===!1||k))return y.abort();if(x="abort",t.add(o.complete),y.done(o.success),y.fail(o.error),e=Nb(Jb,o,c,y)){if(y.readyState=1,l&&q.trigger("ajaxSend",[y,o]),k)return y;o.async&&o.timeout>0&&(i=a.setTimeout(function(){y.abort("timeout")},o.timeout));try{k=!1,e.send(v,A)}catch(z){if(k)throw z;A(-1,z)}}else A(-1,"No Transport");function A(b,c,d,h){var j,m,n,v,w,x=c;k||(k=!0,i&&a.clearTimeout(i),e=void 0,g=h||"",y.readyState=b>0?4:0,j=b>=200&&b<300||304===b,d&&(v=Pb(o,y,d)),v=Qb(o,v,y,j),j?(o.ifModified&&(w=y.getResponseHeader("Last-Modified"),w&&(r.lastModified[f]=w),w=y.getResponseHeader("etag"),w&&(r.etag[f]=w)),204===b||"HEAD"===o.type?x="nocontent":304===b?x="notmodified":(x=v.state,m=v.data,n=v.error,j=!n)):(n=x,!b&&x||(x="error",b<0&&(b=0))),y.status=b,y.statusText=(c||x)+"",j?s.resolveWith(p,[m,x,y]):s.rejectWith(p,[y,x,n]),y.statusCode(u),u=void 0,l&&q.trigger(j?"ajaxSuccess":"ajaxError",[y,o,j?m:n]),t.fireWith(p,[y,x]),l&&(q.trigger("ajaxComplete",[y,o]),--r.active||r.event.trigger("ajaxStop")))}return y},getJSON:function(a,b,c){return r.get(a,b,c,"json")},getScript:function(a,b){return r.get(a,void 0,b,"script")}}),r.each(["get","post"],function(a,b){r[b]=function(a,c,d,e){return r.isFunction(c)&&(e=e||d,d=c,c=void 0),r.ajax(r.extend({url:a,type:b,dataType:e,data:c,success:d},r.isPlainObject(a)&&a))}}),r._evalUrl=function(a){return r.ajax({url:a,type:"GET",dataType:"script",cache:!0,async:!1,global:!1,"throws":!0})},r.fn.extend({wrapAll:function(a){var b;return this[0]&&(r.isFunction(a)&&(a=a.call(this[0])),b=r(a,this[0].ownerDocument).eq(0).clone(!0),this[0].parentNode&&b.insertBefore(this[0]),b.map(function(){var a=this;while(a.firstElementChild)a=a.firstElementChild;return a}).append(this)),this},wrapInner:function(a){return r.isFunction(a)?this.each(function(b){r(this).wrapInner(a.call(this,b))}):this.each(function(){var b=r(this),c=b.contents();c.length?c.wrapAll(a):b.append(a)})},wrap:function(a){var b=r.isFunction(a);return this.each(function(c){r(this).wrapAll(b?a.call(this,c):a)})},unwrap:function(a){return this.parent(a).not("body").each(function(){r(this).replaceWith(this.childNodes)}),this}}),r.expr.pseudos.hidden=function(a){return!r.expr.pseudos.visible(a)},r.expr.pseudos.visible=function(a){return!!(a.offsetWidth||a.offsetHeight||a.getClientRects().length)},r.ajaxSettings.xhr=function(){try{return new a.XMLHttpRequest}catch(b){}};var Rb={0:200,1223:204},Sb=r.ajaxSettings.xhr();o.cors=!!Sb&&"withCredentials"in Sb,o.ajax=Sb=!!Sb,r.ajaxTransport(function(b){var c,d;if(o.cors||Sb&&!b.crossDomain)return{send:function(e,f){var g,h=b.xhr();if(h.open(b.type,b.url,b.async,b.username,b.password),b.xhrFields)for(g in b.xhrFields)h[g]=b.xhrFields[g];b.mimeType&&h.overrideMimeType&&h.overrideMimeType(b.mimeType),b.crossDomain||e["X-Requested-With"]||(e["X-Requested-With"]="XMLHttpRequest");for(g in e)h.setRequestHeader(g,e[g]);c=function(a){return function(){c&&(c=d=h.onload=h.onerror=h.onabort=h.onreadystatechange=null,"abort"===a?h.abort():"error"===a?"number"!=typeof h.status?f(0,"error"):f(h.status,h.statusText):f(Rb[h.status]||h.status,h.statusText,"text"!==(h.responseType||"text")||"string"!=typeof h.responseText?{binary:h.response}:{text:h.responseText},h.getAllResponseHeaders()))}},h.onload=c(),d=h.onerror=c("error"),void 0!==h.onabort?h.onabort=d:h.onreadystatechange=function(){4===h.readyState&&a.setTimeout(function(){c&&d()})},c=c("abort");try{h.send(b.hasContent&&b.data||null)}catch(i){if(c)throw i}},abort:function(){c&&c()}}}),r.ajaxPrefilter(function(a){a.crossDomain&&(a.contents.script=!1)}),r.ajaxSetup({accepts:{script:"text/javascript, application/javascript, application/ecmascript, application/x-ecmascript"},contents:{script:/\b(?:java|ecma)script\b/},converters:{"text script":function(a){return r.globalEval(a),a}}}),r.ajaxPrefilter("script",function(a){void 0===a.cache&&(a.cache=!1),a.crossDomain&&(a.type="GET")}),r.ajaxTransport("script",function(a){if(a.crossDomain){var b,c;return{send:function(e,f){b=r("<script>").prop({charset:a.scriptCharset,src:a.url}).on("load error",c=function(a){b.remove(),c=null,a&&f("error"===a.type?404:200,a.type)}),d.head.appendChild(b[0])},abort:function(){c&&c()}}}});var Tb=[],Ub=/(=)\?(?=&|$)|\?\?/;r.ajaxSetup({jsonp:"callback",jsonpCallback:function(){var a=Tb.pop()||r.expando+"_"+ub++;return this[a]=!0,a}}),r.ajaxPrefilter("json jsonp",function(b,c,d){var e,f,g,h=b.jsonp!==!1&&(Ub.test(b.url)?"url":"string"==typeof b.data&&0===(b.contentType||"").indexOf("application/x-www-form-urlencoded")&&Ub.test(b.data)&&"data");if(h||"jsonp"===b.dataTypes[0])return e=b.jsonpCallback=r.isFunction(b.jsonpCallback)?b.jsonpCallback():b.jsonpCallback,h?b[h]=b[h].replace(Ub,"$1"+e):b.jsonp!==!1&&(b.url+=(vb.test(b.url)?"&":"?")+b.jsonp+"="+e),b.converters["script json"]=function(){return g||r.error(e+" was not called"),g[0]},b.dataTypes[0]="json",f=a[e],a[e]=function(){g=arguments},d.always(function(){void 0===f?r(a).removeProp(e):a[e]=f,b[e]&&(b.jsonpCallback=c.jsonpCallback,Tb.push(e)),g&&r.isFunction(f)&&f(g[0]),g=f=void 0}),"script"}),o.createHTMLDocument=function(){var a=d.implementation.createHTMLDocument("").body;return a.innerHTML="<form></form><form></form>",2===a.childNodes.length}(),r.parseHTML=function(a,b,c){if("string"!=typeof a)return[];"boolean"==typeof b&&(c=b,b=!1);var e,f,g;return b||(o.createHTMLDocument?(b=d.implementation.createHTMLDocument(""),e=b.createElement("base"),e.href=d.location.href,b.head.appendChild(e)):b=d),f=C.exec(a),g=!c&&[],f?[b.createElement(f[1])]:(f=qa([a],b,g),g&&g.length&&r(g).remove(),r.merge([],f.childNodes))},r.fn.load=function(a,b,c){var d,e,f,g=this,h=a.indexOf(" ");return h>-1&&(d=pb(a.slice(h)),a=a.slice(0,h)),r.isFunction(b)?(c=b,b=void 0):b&&"object"==typeof b&&(e="POST"),g.length>0&&r.ajax({url:a,type:e||"GET",dataType:"html",data:b}).done(function(a){f=arguments,g.html(d?r("<div>").append(r.parseHTML(a)).find(d):a)}).always(c&&function(a,b){g.each(function(){c.apply(this,f||[a.responseText,b,a])})}),this},r.each(["ajaxStart","ajaxStop","ajaxComplete","ajaxError","ajaxSuccess","ajaxSend"],function(a,b){r.fn[b]=function(a){return this.on(b,a)}}),r.expr.pseudos.animated=function(a){return r.grep(r.timers,function(b){return a===b.elem}).length},r.offset={setOffset:function(a,b,c){var d,e,f,g,h,i,j,k=r.css(a,"position"),l=r(a),m={};"static"===k&&(a.style.position="relative"),h=l.offset(),f=r.css(a,"top"),i=r.css(a,"left"),j=("absolute"===k||"fixed"===k)&&(f+i).indexOf("auto")>-1,j?(d=l.position(),g=d.top,e=d.left):(g=parseFloat(f)||0,e=parseFloat(i)||0),r.isFunction(b)&&(b=b.call(a,c,r.extend({},h))),null!=b.top&&(m.top=b.top-h.top+g),null!=b.left&&(m.left=b.left-h.left+e),"using"in b?b.using.call(a,m):l.css(m)}},r.fn.extend({offset:function(a){if(arguments.length)return void 0===a?this:this.each(function(b){r.offset.setOffset(this,a,b)});var b,c,d,e,f=this[0];if(f)return f.getClientRects().length?(d=f.getBoundingClientRect(),b=f.ownerDocument,c=b.documentElement,e=b.defaultView,{top:d.top+e.pageYOffset-c.clientTop,left:d.left+e.pageXOffset-c.clientLeft}):{top:0,left:0}},position:function(){if(this[0]){var a,b,c=this[0],d={top:0,left:0};return"fixed"===r.css(c,"position")?b=c.getBoundingClientRect():(a=this.offsetParent(),b=this.offset(),B(a[0],"html")||(d=a.offset()),d={top:d.top+r.css(a[0],"borderTopWidth",!0),left:d.left+r.css(a[0],"borderLeftWidth",!0)}),{top:b.top-d.top-r.css(c,"marginTop",!0),left:b.left-d.left-r.css(c,"marginLeft",!0)}}},offsetParent:function(){return this.map(function(){var a=this.offsetParent;while(a&&"static"===r.css(a,"position"))a=a.offsetParent;return a||ra})}}),r.each({scrollLeft:"pageXOffset",scrollTop:"pageYOffset"},function(a,b){var c="pageYOffset"===b;r.fn[a]=function(d){return T(this,function(a,d,e){var f;return r.isWindow(a)?f=a:9===a.nodeType&&(f=a.defaultView),void 0===e?f?f[b]:a[d]:void(f?f.scrollTo(c?f.pageXOffset:e,c?e:f.pageYOffset):a[d]=e)},a,d,arguments.length)}}),r.each(["top","left"],function(a,b){r.cssHooks[b]=Pa(o.pixelPosition,function(a,c){if(c)return c=Oa(a,b),Ma.test(c)?r(a).position()[b]+"px":c})}),r.each({Height:"height",Width:"width"},function(a,b){r.each({padding:"inner"+a,content:b,"":"outer"+a},function(c,d){r.fn[d]=function(e,f){var g=arguments.length&&(c||"boolean"!=typeof e),h=c||(e===!0||f===!0?"margin":"border");return T(this,function(b,c,e){var f;return r.isWindow(b)?0===d.indexOf("outer")?b["inner"+a]:b.document.documentElement["client"+a]:9===b.nodeType?(f=b.documentElement,Math.max(b.body["scroll"+a],f["scroll"+a],b.body["offset"+a],f["offset"+a],f["client"+a])):void 0===e?r.css(b,c,h):r.style(b,c,e,h)},b,g?e:void 0,g)}})}),r.fn.extend({bind:function(a,b,c){return this.on(a,null,b,c)},unbind:function(a,b){return this.off(a,null,b)},delegate:function(a,b,c,d){return this.on(b,a,c,d)},undelegate:function(a,b,c){return 1===arguments.length?this.off(a,"**"):this.off(b,a||"**",c)}}),r.holdReady=function(a){a?r.readyWait++:r.ready(!0)},r.isArray=Array.isArray,r.parseJSON=JSON.parse,r.nodeName=B,"function"==typeof define&&define.amd&&define("jquery",[],function(){return r});var Vb=a.jQuery,Wb=a.$;return r.noConflict=function(b){return a.$===r&&(a.$=Wb),b&&a.jQuery===r&&(a.jQuery=Vb),r},b||(a.jQuery=a.$=r),r});
;/*! Raven.js 3.13.1 (f55d281) | github.com/getsentry/raven-js */
!function(a){if("object"==typeof exports&&"undefined"!=typeof module)module.exports=a();else if("function"==typeof define&&define.amd)define([],a);else{var b;b="undefined"!=typeof window?window:"undefined"!=typeof global?global:"undefined"!=typeof self?self:this,b.Raven=a()}}(function(){return function a(b,c,d){function e(g,h){if(!c[g]){if(!b[g]){var i="function"==typeof require&&require;if(!h&&i)return i(g,!0);if(f)return f(g,!0);var j=new Error("Cannot find module '"+g+"'");throw j.code="MODULE_NOT_FOUND",j}var k=c[g]={exports:{}};b[g][0].call(k.exports,function(a){var c=b[g][1][a];return e(c?c:a)},k,k.exports,a,b,c,d)}return c[g].exports}for(var f="function"==typeof require&&require,g=0;g<d.length;g++)e(d[g]);return e}({1:[function(a,b,c){"use strict";function d(a){this.name="RavenConfigError",this.message=a}d.prototype=new Error,d.prototype.constructor=d,b.exports=d},{}],2:[function(a,b,c){"use strict";var d=function(a,b,c){var d=a[b],e=a;if(b in a){var f="warn"===b?"warning":b;a[b]=function(){var a=[].slice.call(arguments),b=""+a.join(" "),g={level:f,logger:"console",extra:{arguments:a}};c&&c(b,g),d&&Function.prototype.apply.call(d,e,a)}}};b.exports={wrapMethod:d}},{}],3:[function(a,b,c){(function(c){"use strict";function d(){return+new Date}function e(){this.a=!("object"!=typeof JSON||!JSON.stringify),this.b=!f(H),this.c=!f(I),this.d=null,this.e=null,this.f=null,this.g=null,this.h=null,this.i=null,this.j={},this.k={logger:"javascript",ignoreErrors:[],ignoreUrls:[],whitelistUrls:[],includePaths:[],crossOrigin:"anonymous",collectWindowErrors:!0,maxMessageLength:0,stackTraceLimit:50,autoBreadcrumbs:!0,sampleRate:1},this.l=0,this.m=!1,this.n=Error.stackTraceLimit,this.o=G.console||{},this.p={},this.q=[],this.r=d(),this.s=[],this.t=[],this.u=null,this.v=G.location,this.w=this.v&&this.v.href,this.x();for(var a in this.o)this.p[a]=this.o[a]}function f(a){return void 0===a}function g(a){return"function"==typeof a}function h(a){return"[object String]"===J.toString.call(a)}function i(a){for(var b in a)return!1;return!0}function j(a,b){var c,d;if(f(a.length))for(c in a)m(a,c)&&b.call(null,c,a[c]);else if(d=a.length)for(c=0;c<d;c++)b.call(null,c,a[c])}function k(a,b){return b?(j(b,function(b,c){a[b]=c}),a):a}function l(a,b){return!b||a.length<=b?a:a.substr(0,b)+"…"}function m(a,b){return J.hasOwnProperty.call(a,b)}function n(a){for(var b,c=[],d=0,e=a.length;d<e;d++)b=a[d],h(b)?c.push(b.replace(/([.*+?^=!:${}()|\[\]\/\\])/g,"\\$1")):b&&b.source&&c.push(b.source);return new RegExp(c.join("|"),"i")}function o(a){var b=[];return j(a,function(a,c){b.push(encodeURIComponent(a)+"="+encodeURIComponent(c))}),b.join("&")}function p(a){var b=a.match(/^(([^:\/?#]+):)?(\/\/([^\/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?$/);if(!b)return{};var c=b[6]||"",d=b[8]||"";return{protocol:b[2],host:b[4],path:b[5],relative:b[5]+c+d}}function q(){var a=G.crypto||G.msCrypto;if(!f(a)&&a.getRandomValues){var b=new Uint16Array(8);a.getRandomValues(b),b[3]=4095&b[3]|16384,b[4]=16383&b[4]|32768;var c=function(a){for(var b=a.toString(16);b.length<4;)b="0"+b;return b};return c(b[0])+c(b[1])+c(b[2])+c(b[3])+c(b[4])+c(b[5])+c(b[6])+c(b[7])}return"xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx".replace(/[xy]/g,function(a){var b=16*Math.random()|0,c="x"===a?b:3&b|8;return c.toString(16)})}function r(a){for(var b,c=5,d=80,e=[],f=0,g=0,h=" > ",i=h.length;a&&f++<c&&(b=s(a),!("html"===b||f>1&&g+e.length*i+b.length>=d));)e.push(b),g+=b.length,a=a.parentNode;return e.reverse().join(h)}function s(a){var b,c,d,e,f,g=[];if(!a||!a.tagName)return"";if(g.push(a.tagName.toLowerCase()),a.id&&g.push("#"+a.id),b=a.className,b&&h(b))for(c=b.split(/\s+/),f=0;f<c.length;f++)g.push("."+c[f]);var i=["type","name","title","alt"];for(f=0;f<i.length;f++)d=i[f],e=a.getAttribute(d),e&&g.push("["+d+'="'+e+'"]');return g.join("")}function t(a,b){return!!(!!a^!!b)}function u(a,b){return!t(a,b)&&(a=a.values[0],b=b.values[0],a.type===b.type&&a.value===b.value&&v(a.stacktrace,b.stacktrace))}function v(a,b){if(t(a,b))return!1;var c=a.frames,d=b.frames;if(c.length!==d.length)return!1;for(var e,f,g=0;g<c.length;g++)if(e=c[g],f=d[g],e.filename!==f.filename||e.lineno!==f.lineno||e.colno!==f.colno||e["function"]!==f["function"])return!1;return!0}function w(a,b,c,d){var e=a[b];a[b]=c(e),d&&d.push([a,b,e])}var x=a(6),y=a(7),z=a(1),A=a(5),B=A.isError,C=A.isObject,D=a(2).wrapMethod,E="source protocol user pass host port path".split(" "),F=/^(?:(\w+):)?\/\/(?:(\w+)(:\w+)?@)?([\w\.-]+)(?::(\d+))?(\/.*)/,G="undefined"!=typeof window?window:"undefined"!=typeof c?c:"undefined"!=typeof self?self:{},H=G.document,I=G.navigator;e.prototype={VERSION:"3.13.1",debug:!1,TraceKit:x,config:function(a,b){var c=this;if(c.g)return this.y("error","Error: Raven has already been configured"),c;if(!a)return c;var d=c.k;b&&j(b,function(a,b){"tags"===a||"extra"===a||"user"===a?c.j[a]=b:d[a]=b}),c.setDSN(a),d.ignoreErrors.push(/^Script error\.?$/),d.ignoreErrors.push(/^Javascript error: Script error\.? on line 0$/),d.ignoreErrors=n(d.ignoreErrors),d.ignoreUrls=!!d.ignoreUrls.length&&n(d.ignoreUrls),d.whitelistUrls=!!d.whitelistUrls.length&&n(d.whitelistUrls),d.includePaths=n(d.includePaths),d.maxBreadcrumbs=Math.max(0,Math.min(d.maxBreadcrumbs||100,100));var e={xhr:!0,console:!0,dom:!0,location:!0},f=d.autoBreadcrumbs;return"[object Object]"==={}.toString.call(f)?f=k(e,f):f!==!1&&(f=e),d.autoBreadcrumbs=f,x.collectWindowErrors=!!d.collectWindowErrors,c},install:function(){var a=this;return a.isSetup()&&!a.m&&(x.report.subscribe(function(){a.z.apply(a,arguments)}),a.A(),a.k.autoBreadcrumbs&&a.B(),a.C(),a.m=!0),Error.stackTraceLimit=a.k.stackTraceLimit,this},setDSN:function(a){var b=this,c=b.D(a),d=c.path.lastIndexOf("/"),e=c.path.substr(1,d);b.E=a,b.h=c.user,b.F=c.pass&&c.pass.substr(1),b.i=c.path.substr(d+1),b.g=b.G(c),b.H=b.g+"/"+e+"api/"+b.i+"/store/",this.x()},context:function(a,b,c){return g(a)&&(c=b||[],b=a,a=void 0),this.wrap(a,b).apply(this,c)},wrap:function(a,b,c){function d(){var d=[],f=arguments.length,h=!a||a&&a.deep!==!1;for(c&&g(c)&&c.apply(this,arguments);f--;)d[f]=h?e.wrap(a,arguments[f]):arguments[f];try{return b.apply(this,d)}catch(i){throw e.I(),e.captureException(i,a),i}}var e=this;if(f(b)&&!g(a))return a;if(g(a)&&(b=a,a=void 0),!g(b))return b;try{if(b.J)return b;if(b.K)return b.K}catch(h){return b}for(var i in b)m(b,i)&&(d[i]=b[i]);return d.prototype=b.prototype,b.K=d,d.J=!0,d.L=b,d},uninstall:function(){return x.report.uninstall(),this.M(),Error.stackTraceLimit=this.n,this.m=!1,this},captureException:function(a,b){if(!B(a))return this.captureMessage(a,k({trimHeadFrames:1,stacktrace:!0},b));this.d=a;try{var c=x.computeStackTrace(a);this.N(c,b)}catch(d){if(a!==d)throw d}return this},captureMessage:function(a,b){if(!this.k.ignoreErrors.test||!this.k.ignoreErrors.test(a)){b=b||{};var c=k({message:a+""},b);if(this.k.stacktrace||b&&b.stacktrace){var d;try{throw new Error(a)}catch(e){d=e}d.name=null,b=k({fingerprint:a,trimHeadFrames:(b.trimHeadFrames||0)+1},b);var f=x.computeStackTrace(d),g=this.O(f,b);c.stacktrace={frames:g.reverse()}}return this.P(c),this}},captureBreadcrumb:function(a){var b=k({timestamp:d()/1e3},a);if(g(this.k.breadcrumbCallback)){var c=this.k.breadcrumbCallback(b);if(C(c)&&!i(c))b=c;else if(c===!1)return this}return this.t.push(b),this.t.length>this.k.maxBreadcrumbs&&this.t.shift(),this},addPlugin:function(a){var b=[].slice.call(arguments,1);return this.q.push([a,b]),this.m&&this.C(),this},setUserContext:function(a){return this.j.user=a,this},setExtraContext:function(a){return this.Q("extra",a),this},setTagsContext:function(a){return this.Q("tags",a),this},clearContext:function(){return this.j={},this},getContext:function(){return JSON.parse(y(this.j))},setEnvironment:function(a){return this.k.environment=a,this},setRelease:function(a){return this.k.release=a,this},setDataCallback:function(a){var b=this.k.dataCallback;return this.k.dataCallback=g(a)?function(c){return a(c,b)}:a,this},setBreadcrumbCallback:function(a){var b=this.k.breadcrumbCallback;return this.k.breadcrumbCallback=g(a)?function(c){return a(c,b)}:a,this},setShouldSendCallback:function(a){var b=this.k.shouldSendCallback;return this.k.shouldSendCallback=g(a)?function(c){return a(c,b)}:a,this},setTransport:function(a){return this.k.transport=a,this},lastException:function(){return this.d},lastEventId:function(){return this.f},isSetup:function(){return!!this.a&&(!!this.g||(this.ravenNotConfiguredError||(this.ravenNotConfiguredError=!0,this.y("error","Error: Raven has not been configured.")),!1))},afterLoad:function(){var a=G.RavenConfig;a&&this.config(a.dsn,a.config).install()},showReportDialog:function(a){if(H){a=a||{};var b=a.eventId||this.lastEventId();if(!b)throw new z("Missing eventId");var c=a.dsn||this.E;if(!c)throw new z("Missing DSN");var d=encodeURIComponent,e="";e+="?eventId="+d(b),e+="&dsn="+d(c);var f=a.user||this.j.user;f&&(f.name&&(e+="&name="+d(f.name)),f.email&&(e+="&email="+d(f.email)));var g=this.G(this.D(c)),h=H.createElement("script");h.async=!0,h.src=g+"/api/embed/error-page/"+e,(H.head||H.body).appendChild(h)}},I:function(){var a=this;this.l+=1,setTimeout(function(){a.l-=1})},R:function(a,b){var c,d;if(this.b){b=b||{},a="raven"+a.substr(0,1).toUpperCase()+a.substr(1),H.createEvent?(c=H.createEvent("HTMLEvents"),c.initEvent(a,!0,!0)):(c=H.createEventObject(),c.eventType=a);for(d in b)m(b,d)&&(c[d]=b[d]);if(H.createEvent)H.dispatchEvent(c);else try{H.fireEvent("on"+c.eventType.toLowerCase(),c)}catch(e){}}},S:function(a){var b=this;return function(c){if(b.T=null,b.u!==c){b.u=c;var d;try{d=r(c.target)}catch(e){d="<unknown>"}b.captureBreadcrumb({category:"ui."+a,message:d})}}},U:function(){var a=this,b=1e3;return function(c){var d;try{d=c.target}catch(e){return}var f=d&&d.tagName;if(f&&("INPUT"===f||"TEXTAREA"===f||d.isContentEditable)){var g=a.T;g||a.S("input")(c),clearTimeout(g),a.T=setTimeout(function(){a.T=null},b)}}},V:function(a,b){var c=p(this.v.href),d=p(b),e=p(a);this.w=b,c.protocol===d.protocol&&c.host===d.host&&(b=d.relative),c.protocol===e.protocol&&c.host===e.host&&(a=e.relative),this.captureBreadcrumb({category:"navigation",data:{to:b,from:a}})},A:function(){function a(a){return function(b,d){for(var e=new Array(arguments.length),f=0;f<e.length;++f)e[f]=arguments[f];var h=e[0];return g(h)&&(e[0]=c.wrap(h)),a.apply?a.apply(this,e):a(e[0],e[1])}}function b(a){var b=G[a]&&G[a].prototype;b&&b.hasOwnProperty&&b.hasOwnProperty("addEventListener")&&(w(b,"addEventListener",function(b){return function(d,f,g,h){try{f&&f.handleEvent&&(f.handleEvent=c.wrap(f.handleEvent))}catch(i){}var j,k,l;return e&&e.dom&&("EventTarget"===a||"Node"===a)&&(k=c.S("click"),l=c.U(),j=function(a){if(a){var b;try{b=a.type}catch(c){return}return"click"===b?k(a):"keypress"===b?l(a):void 0}}),b.call(this,d,c.wrap(f,void 0,j),g,h)}},d),w(b,"removeEventListener",function(a){return function(b,c,d,e){try{c=c&&(c.K?c.K:c)}catch(f){}return a.call(this,b,c,d,e)}},d))}var c=this,d=c.s,e=this.k.autoBreadcrumbs;w(G,"setTimeout",a,d),w(G,"setInterval",a,d),G.requestAnimationFrame&&w(G,"requestAnimationFrame",function(a){return function(b){return a(c.wrap(b))}},d);for(var f=["EventTarget","Window","Node","ApplicationCache","AudioTrackList","ChannelMergerNode","CryptoOperation","EventSource","FileReader","HTMLUnknownElement","IDBDatabase","IDBRequest","IDBTransaction","KeyOperation","MediaController","MessagePort","ModalWindow","Notification","SVGElementInstance","Screen","TextTrack","TextTrackCue","TextTrackList","WebSocket","WebSocketWorker","Worker","XMLHttpRequest","XMLHttpRequestEventTarget","XMLHttpRequestUpload"],h=0;h<f.length;h++)b(f[h])},B:function(){function a(a,c){a in c&&g(c[a])&&w(c,a,function(a){return b.wrap(a)})}var b=this,c=this.k.autoBreadcrumbs,d=b.s;if(c.xhr&&"XMLHttpRequest"in G){var e=XMLHttpRequest.prototype;w(e,"open",function(a){return function(c,d){return h(d)&&d.indexOf(b.h)===-1&&(this.W={method:c,url:d,status_code:null}),a.apply(this,arguments)}},d),w(e,"send",function(c){return function(d){function e(){if(f.W&&(1===f.readyState||4===f.readyState)){try{f.W.status_code=f.status}catch(a){}b.captureBreadcrumb({type:"http",category:"xhr",data:f.W})}}for(var f=this,h=["onload","onerror","onprogress"],i=0;i<h.length;i++)a(h[i],f);return"onreadystatechange"in f&&g(f.onreadystatechange)?w(f,"onreadystatechange",function(a){return b.wrap(a,void 0,e)}):f.onreadystatechange=e,c.apply(this,arguments)}},d)}c.xhr&&"fetch"in G&&w(G,"fetch",function(a){return function(c,d){for(var e=new Array(arguments.length),f=0;f<e.length;++f)e[f]=arguments[f];var g="GET";e[1]&&e[1].method&&(g=e[1].method);var h={method:g,url:e[0],status_code:null};return b.captureBreadcrumb({type:"http",category:"fetch",data:h}),a.apply(this,e).then(function(a){return h.status_code=a.status,a})}},d),c.dom&&this.b&&(H.addEventListener?(H.addEventListener("click",b.S("click"),!1),H.addEventListener("keypress",b.U(),!1)):(H.attachEvent("onclick",b.S("click")),H.attachEvent("onkeypress",b.U())));var f=G.chrome,i=f&&f.app&&f.app.runtime,k=!i&&G.history&&history.pushState;if(c.location&&k){var l=G.onpopstate;G.onpopstate=function(){var a=b.v.href;if(b.V(b.w,a),l)return l.apply(this,arguments)},w(history,"pushState",function(a){return function(){var c=arguments.length>2?arguments[2]:void 0;return c&&b.V(b.w,c+""),a.apply(this,arguments)}},d)}if(c.console&&"console"in G&&console.log){var m=function(a,c){b.captureBreadcrumb({message:a,level:c.level,category:"console"})};j(["debug","info","warn","error","log"],function(a,b){D(console,b,m)})}},M:function(){for(var a;this.s.length;){a=this.s.shift();var b=a[0],c=a[1],d=a[2];b[c]=d}},C:function(){var a=this;j(this.q,function(b,c){var d=c[0],e=c[1];d.apply(a,[a].concat(e))})},D:function(a){var b=F.exec(a),c={},d=7;try{for(;d--;)c[E[d]]=b[d]||""}catch(e){throw new z("Invalid DSN: "+a)}if(c.pass&&!this.k.allowSecretKey)throw new z("Do not specify your secret key in the DSN. See: http://bit.ly/raven-secret-key");return c},G:function(a){var b="//"+a.host+(a.port?":"+a.port:"");return a.protocol&&(b=a.protocol+":"+b),b},z:function(){this.l||this.N.apply(this,arguments)},N:function(a,b){var c=this.O(a,b);this.R("handle",{stackInfo:a,options:b}),this.X(a.name,a.message,a.url,a.lineno,c,b)},O:function(a,b){var c=this,d=[];if(a.stack&&a.stack.length&&(j(a.stack,function(a,b){var e=c.Y(b);e&&d.push(e)}),b&&b.trimHeadFrames))for(var e=0;e<b.trimHeadFrames&&e<d.length;e++)d[e].in_app=!1;return d=d.slice(0,this.k.stackTraceLimit)},Y:function(a){if(a.url){var b={filename:a.url,lineno:a.line,colno:a.column,"function":a.func||"?"};return b.in_app=!(this.k.includePaths.test&&!this.k.includePaths.test(b.filename)||/(Raven|TraceKit)\./.test(b["function"])||/raven\.(min\.)?js$/.test(b.filename)),b}},X:function(a,b,c,d,e,f){var g;if((!this.k.ignoreErrors.test||!this.k.ignoreErrors.test(b))&&(b+="",e&&e.length?(c=e[0].filename||c,e.reverse(),g={frames:e}):c&&(g={frames:[{filename:c,lineno:d,in_app:!0}]}),(!this.k.ignoreUrls.test||!this.k.ignoreUrls.test(c))&&(!this.k.whitelistUrls.test||this.k.whitelistUrls.test(c)))){var h=k({exception:{values:[{type:a,value:b,stacktrace:g}]},culprit:c},f);this.P(h)}},Z:function(a){var b=this.k.maxMessageLength;if(a.message&&(a.message=l(a.message,b)),a.exception){var c=a.exception.values[0];c.value=l(c.value,b)}return a},$:function(){if(this.c||this.b){var a={};return this.c&&I.userAgent&&(a.headers={"User-Agent":navigator.userAgent}),this.b&&(H.location&&H.location.href&&(a.url=H.location.href),H.referrer&&(a.headers||(a.headers={}),a.headers.Referer=H.referrer)),a}},x:function(){this._=0,this.aa=null},ba:function(){return this._&&d()-this.aa<this._},ca:function(a){var b=this.e;return!(!b||a.message!==b.message||a.culprit!==b.culprit)&&(a.stacktrace||b.stacktrace?v(a.stacktrace,b.stacktrace):!a.exception&&!b.exception||u(a.exception,b.exception))},da:function(a){if(!this.ba()){var b=a.status;if(400===b||401===b||429===b){var c;try{c=a.getResponseHeader("Retry-After"),c=1e3*parseInt(c,10)}catch(e){}this._=c?c:2*this._||1e3,this.aa=d()}}},P:function(a){var b=this.k,c={project:this.i,logger:b.logger,platform:"javascript"},e=this.$();if(e&&(c.request=e),a.trimHeadFrames&&delete a.trimHeadFrames,a=k(c,a),a.tags=k(k({},this.j.tags),a.tags),a.extra=k(k({},this.j.extra),a.extra),a.extra["session:duration"]=d()-this.r,this.t&&this.t.length>0&&(a.breadcrumbs={values:[].slice.call(this.t,0)}),i(a.tags)&&delete a.tags,this.j.user&&(a.user=this.j.user),b.environment&&(a.environment=b.environment),b.release&&(a.release=b.release),b.serverName&&(a.server_name=b.serverName),g(b.dataCallback)&&(a=b.dataCallback(a)||a),a&&!i(a)&&(!g(b.shouldSendCallback)||b.shouldSendCallback(a)))return this.ba()?void this.y("warn","Raven dropped error due to backoff: ",a):void("number"==typeof b.sampleRate?Math.random()<b.sampleRate&&this.ea(a):this.ea(a))},fa:function(){return q()},ea:function(a,b){var c=this,d=this.k;if(this.isSetup()){if(this.f=a.event_id||(a.event_id=this.fa()),a=this.Z(a),!this.k.allowDuplicates&&this.ca(a))return void this.y("warn","Raven dropped repeat event: ",a);this.e=a,this.y("debug","Raven about to send:",a);var e={sentry_version:"7",sentry_client:"raven-js/"+this.VERSION,sentry_key:this.h};this.F&&(e.sentry_secret=this.F);var f=a.exception&&a.exception.values[0];this.captureBreadcrumb({category:"sentry",message:f?(f.type?f.type+": ":"")+f.value:a.message,event_id:a.event_id,level:a.level||"error"});var g=this.H;(d.transport||this.ga).call(this,{url:g,auth:e,data:a,options:d,onSuccess:function(){c.x(),c.R("success",{data:a,src:g}),b&&b()},onError:function(d){c.y("error","Raven transport failed to send: ",d),d.request&&c.da(d.request),c.R("failure",{data:a,src:g}),d=d||new Error("Raven send failed (no additional details provided)"),b&&b(d)}})}},ga:function(a){var b=new XMLHttpRequest,c="withCredentials"in b||"undefined"!=typeof XDomainRequest;if(c){var d=a.url;"withCredentials"in b?b.onreadystatechange=function(){if(4===b.readyState)if(200===b.status)a.onSuccess&&a.onSuccess();else if(a.onError){var c=new Error("Sentry error code: "+b.status);c.request=b,a.onError(c)}}:(b=new XDomainRequest,d=d.replace(/^https?:/,""),a.onSuccess&&(b.onload=a.onSuccess),a.onError&&(b.onerror=function(){var c=new Error("Sentry error code: XDomainRequest");c.request=b,a.onError(c)})),b.open("POST",d+"?"+o(a.auth)),b.send(y(a.data))}},y:function(a){this.p[a]&&this.debug&&Function.prototype.apply.call(this.p[a],this.o,[].slice.call(arguments,1))},Q:function(a,b){f(b)?delete this.j[a]:this.j[a]=k(this.j[a]||{},b)}};var J=Object.prototype;e.prototype.setUser=e.prototype.setUserContext,e.prototype.setReleaseContext=e.prototype.setRelease,b.exports=e}).call(this,"undefined"!=typeof global?global:"undefined"!=typeof self?self:"undefined"!=typeof window?window:{})},{1:1,2:2,5:5,6:6,7:7}],4:[function(a,b,c){(function(c){"use strict";var d=a(3),e="undefined"!=typeof window?window:"undefined"!=typeof c?c:"undefined"!=typeof self?self:{},f=e.Raven,g=new d;g.noConflict=function(){return e.Raven=f,g},g.afterLoad(),b.exports=g}).call(this,"undefined"!=typeof global?global:"undefined"!=typeof self?self:"undefined"!=typeof window?window:{})},{3:3}],5:[function(a,b,c){"use strict";function d(a){return"object"==typeof a&&null!==a}function e(a){var b={}.toString.call(a);return d(a)&&"[object Error]"===b||"[object Exception]"===b||a instanceof Error}b.exports={isObject:d,isError:e}},{}],6:[function(a,b,c){(function(c){"use strict";function d(){return"undefined"==typeof document||"undefined"==typeof document.location?"":document.location.href}var e=a(5),f={collectWindowErrors:!0,debug:!1},g="undefined"!=typeof window?window:"undefined"!=typeof c?c:"undefined"!=typeof self?self:{},h=[].slice,i="?",j=/^(?:[Uu]ncaught (?:exception: )?)?(?:((?:Eval|Internal|Range|Reference|Syntax|Type|URI|)Error): )?(.*)$/;f.report=function(){function a(a){m(),s.push(a)}function b(a){for(var b=s.length-1;b>=0;--b)s[b]===a&&s.splice(b,1)}function c(){n(),s=[]}function k(a,b){var c=null;if(!b||f.collectWindowErrors){for(var d in s)if(s.hasOwnProperty(d))try{s[d].apply(null,[a].concat(h.call(arguments,2)))}catch(e){c=e}if(c)throw c}}function l(a,b,c,g,h){var l=null;if(v)f.computeStackTrace.augmentStackTraceWithInitialElement(v,b,c,a),o();else if(h&&e.isError(h))l=f.computeStackTrace(h),k(l,!0);else{var m,n={url:b,line:c,column:g},p=void 0,r=a;if("[object String]"==={}.toString.call(a)){var m=a.match(j);m&&(p=m[1],r=m[2])}n.func=i,l={name:p,message:r,url:d(),stack:[n]},k(l,!0)}return!!q&&q.apply(this,arguments)}function m(){r||(q=g.onerror,g.onerror=l,r=!0)}function n(){r&&(g.onerror=q,r=!1,q=void 0)}function o(){var a=v,b=t;t=null,v=null,u=null,k.apply(null,[a,!1].concat(b))}function p(a,b){var c=h.call(arguments,1);if(v){if(u===a)return;o()}var d=f.computeStackTrace(a);if(v=d,u=a,t=c,setTimeout(function(){u===a&&o()},d.incomplete?2e3:0),b!==!1)throw a}var q,r,s=[],t=null,u=null,v=null;return p.subscribe=a,p.unsubscribe=b,p.uninstall=c,p}(),f.computeStackTrace=function(){function a(a){if("undefined"!=typeof a.stack&&a.stack){for(var b,c,e=/^\s*at (.*?) ?\(((?:file|https?|blob|chrome-extension|native|eval|<anonymous>).*?)(?::(\d+))?(?::(\d+))?\)?\s*$/i,f=/^\s*(.*?)(?:\((.*?)\))?(?:^|@)((?:file|https?|blob|chrome|resource|\[native).*?)(?::(\d+))?(?::(\d+))?\s*$/i,g=/^\s*at (?:((?:\[object object\])?.+) )?\(?((?:file|ms-appx|https?|blob):.*?):(\d+)(?::(\d+))?\)?\s*$/i,h=a.stack.split("\n"),j=[],k=(/^(.*) is undefined$/.exec(a.message),0),l=h.length;k<l;++k){if(b=e.exec(h[k])){var m=b[2]&&b[2].indexOf("native")!==-1;c={url:m?null:b[2],func:b[1]||i,args:m?[b[2]]:[],line:b[3]?+b[3]:null,column:b[4]?+b[4]:null}}else if(b=g.exec(h[k]))c={url:b[2],func:b[1]||i,args:[],line:+b[3],column:b[4]?+b[4]:null};else{if(!(b=f.exec(h[k])))continue;c={url:b[3],func:b[1]||i,args:b[2]?b[2].split(","):[],line:b[4]?+b[4]:null,column:b[5]?+b[5]:null}}!c.func&&c.line&&(c.func=i),j.push(c)}return j.length?(j[0].column||"undefined"==typeof a.columnNumber||(j[0].column=a.columnNumber+1),{name:a.name,message:a.message,url:d(),stack:j}):null}}function b(a,b,c,d){var e={url:b,line:c};if(e.url&&e.line){if(a.incomplete=!1,e.func||(e.func=i),a.stack.length>0&&a.stack[0].url===e.url){if(a.stack[0].line===e.line)return!1;if(!a.stack[0].line&&a.stack[0].func===e.func)return a.stack[0].line=e.line,!1}return a.stack.unshift(e),a.partial=!0,!0}return a.incomplete=!0,!1}function c(a,g){for(var h,j,k=/function\s+([_$a-zA-Z\xA0-\uFFFF][_$a-zA-Z0-9\xA0-\uFFFF]*)?\s*\(/i,l=[],m={},n=!1,o=c.caller;o&&!n;o=o.caller)if(o!==e&&o!==f.report){if(j={url:null,func:i,line:null,column:null},o.name?j.func=o.name:(h=k.exec(o.toString()))&&(j.func=h[1]),"undefined"==typeof j.func)try{j.func=h.input.substring(0,h.input.indexOf("{"))}catch(p){}m[""+o]?n=!0:m[""+o]=!0,l.push(j)}g&&l.splice(0,g);var q={name:a.name,message:a.message,url:d(),stack:l};return b(q,a.sourceURL||a.fileName,a.line||a.lineNumber,a.message||a.description),q}function e(b,e){var g=null;e=null==e?0:+e;try{if(g=a(b))return g}catch(h){if(f.debug)throw h}try{if(g=c(b,e+1))return g}catch(h){if(f.debug)throw h}return{name:b.name,message:b.message,url:d()}}return e.augmentStackTraceWithInitialElement=b,e.computeStackTraceFromStackProp=a,e}(),b.exports=f}).call(this,"undefined"!=typeof global?global:"undefined"!=typeof self?self:"undefined"!=typeof window?window:{})},{5:5}],7:[function(a,b,c){"use strict";function d(a,b){for(var c=0;c<a.length;++c)if(a[c]===b)return c;return-1}function e(a,b,c,d){return JSON.stringify(a,f(b,d),c)}function f(a,b){var c=[],e=[];return null==b&&(b=function(a,b){return c[0]===b?"[Circular ~]":"[Circular ~."+e.slice(0,d(c,b)).join(".")+"]"}),function(f,g){if(c.length>0){var h=d(c,this);~h?c.splice(h+1):c.push(this),~h?e.splice(h,1/0,f):e.push(f),~d(c,g)&&(g=b.call(this,f,g))}else c.push(g);return null==a?g:a.call(this,f,g)}}c=b.exports=e,c.getSerialize=f},{}]},{},[4])(4)});
//# sourceMappingURL=raven.min.js.map;//     Underscore.js 1.8.3
//     http://underscorejs.org
//     (c) 2009-2015 Jeremy Ashkenas, DocumentCloud and Investigative Reporters & Editors
//     Underscore may be freely distributed under the MIT license.

(function() {

  // Baseline setup
  // --------------

  // Establish the root object, `window` in the browser, or `exports` on the server.
  var root = this;

  // Save the previous value of the `_` variable.
  var previousUnderscore = root._;

  // Save bytes in the minified (but not gzipped) version:
  var ArrayProto = Array.prototype, ObjProto = Object.prototype, FuncProto = Function.prototype;

  // Create quick reference variables for speed access to core prototypes.
  var
    push             = ArrayProto.push,
    slice            = ArrayProto.slice,
    toString         = ObjProto.toString,
    hasOwnProperty   = ObjProto.hasOwnProperty;

  // All **ECMAScript 5** native function implementations that we hope to use
  // are declared here.
  var
    nativeIsArray      = Array.isArray,
    nativeKeys         = Object.keys,
    nativeBind         = FuncProto.bind,
    nativeCreate       = Object.create;

  // Naked function reference for surrogate-prototype-swapping.
  var Ctor = function(){};

  // Create a safe reference to the Underscore object for use below.
  var _ = function(obj) {
    if (obj instanceof _) return obj;
    if (!(this instanceof _)) return new _(obj);
    this._wrapped = obj;
  };

  // Export the Underscore object for **Node.js**, with
  // backwards-compatibility for the old `require()` API. If we're in
  // the browser, add `_` as a global object.
  if (typeof exports !== 'undefined') {
    if (typeof module !== 'undefined' && module.exports) {
      exports = module.exports = _;
    }
    exports._ = _;
  } else {
    root._ = _;
  }

  // Current version.
  _.VERSION = '1.8.3';

  // Internal function that returns an efficient (for current engines) version
  // of the passed-in callback, to be repeatedly applied in other Underscore
  // functions.
  var optimizeCb = function(func, context, argCount) {
    if (context === void 0) return func;
    switch (argCount == null ? 3 : argCount) {
      case 1: return function(value) {
        return func.call(context, value);
      };
      case 2: return function(value, other) {
        return func.call(context, value, other);
      };
      case 3: return function(value, index, collection) {
        return func.call(context, value, index, collection);
      };
      case 4: return function(accumulator, value, index, collection) {
        return func.call(context, accumulator, value, index, collection);
      };
    }
    return function() {
      return func.apply(context, arguments);
    };
  };

  // A mostly-internal function to generate callbacks that can be applied
  // to each element in a collection, returning the desired result — either
  // identity, an arbitrary callback, a property matcher, or a property accessor.
  var cb = function(value, context, argCount) {
    if (value == null) return _.identity;
    if (_.isFunction(value)) return optimizeCb(value, context, argCount);
    if (_.isObject(value)) return _.matcher(value);
    return _.property(value);
  };
  _.iteratee = function(value, context) {
    return cb(value, context, Infinity);
  };

  // An internal function for creating assigner functions.
  var createAssigner = function(keysFunc, undefinedOnly) {
    return function(obj) {
      var length = arguments.length;
      if (length < 2 || obj == null) return obj;
      for (var index = 1; index < length; index++) {
        var source = arguments[index],
            keys = keysFunc(source),
            l = keys.length;
        for (var i = 0; i < l; i++) {
          var key = keys[i];
          if (!undefinedOnly || obj[key] === void 0) obj[key] = source[key];
        }
      }
      return obj;
    };
  };

  // An internal function for creating a new object that inherits from another.
  var baseCreate = function(prototype) {
    if (!_.isObject(prototype)) return {};
    if (nativeCreate) return nativeCreate(prototype);
    Ctor.prototype = prototype;
    var result = new Ctor;
    Ctor.prototype = null;
    return result;
  };

  var property = function(key) {
    return function(obj) {
      return obj == null ? void 0 : obj[key];
    };
  };

  // Helper for collection methods to determine whether a collection
  // should be iterated as an array or as an object
  // Related: http://people.mozilla.org/~jorendorff/es6-draft.html#sec-tolength
  // Avoids a very nasty iOS 8 JIT bug on ARM-64. #2094
  var MAX_ARRAY_INDEX = Math.pow(2, 53) - 1;
  var getLength = property('length');
  var isArrayLike = function(collection) {
    var length = getLength(collection);
    return typeof length == 'number' && length >= 0 && length <= MAX_ARRAY_INDEX;
  };

  // Collection Functions
  // --------------------

  // The cornerstone, an `each` implementation, aka `forEach`.
  // Handles raw objects in addition to array-likes. Treats all
  // sparse array-likes as if they were dense.
  _.each = _.forEach = function(obj, iteratee, context) {
    iteratee = optimizeCb(iteratee, context);
    var i, length;
    if (isArrayLike(obj)) {
      for (i = 0, length = obj.length; i < length; i++) {
        iteratee(obj[i], i, obj);
      }
    } else {
      var keys = _.keys(obj);
      for (i = 0, length = keys.length; i < length; i++) {
        iteratee(obj[keys[i]], keys[i], obj);
      }
    }
    return obj;
  };

  // Return the results of applying the iteratee to each element.
  _.map = _.collect = function(obj, iteratee, context) {
    iteratee = cb(iteratee, context);
    var keys = !isArrayLike(obj) && _.keys(obj),
        length = (keys || obj).length,
        results = Array(length);
    for (var index = 0; index < length; index++) {
      var currentKey = keys ? keys[index] : index;
      results[index] = iteratee(obj[currentKey], currentKey, obj);
    }
    return results;
  };

  // Create a reducing function iterating left or right.
  function createReduce(dir) {
    // Optimized iterator function as using arguments.length
    // in the main function will deoptimize the, see #1991.
    function iterator(obj, iteratee, memo, keys, index, length) {
      for (; index >= 0 && index < length; index += dir) {
        var currentKey = keys ? keys[index] : index;
        memo = iteratee(memo, obj[currentKey], currentKey, obj);
      }
      return memo;
    }

    return function(obj, iteratee, memo, context) {
      iteratee = optimizeCb(iteratee, context, 4);
      var keys = !isArrayLike(obj) && _.keys(obj),
          length = (keys || obj).length,
          index = dir > 0 ? 0 : length - 1;
      // Determine the initial value if none is provided.
      if (arguments.length < 3) {
        memo = obj[keys ? keys[index] : index];
        index += dir;
      }
      return iterator(obj, iteratee, memo, keys, index, length);
    };
  }

  // **Reduce** builds up a single result from a list of values, aka `inject`,
  // or `foldl`.
  _.reduce = _.foldl = _.inject = createReduce(1);

  // The right-associative version of reduce, also known as `foldr`.
  _.reduceRight = _.foldr = createReduce(-1);

  // Return the first value which passes a truth test. Aliased as `detect`.
  _.find = _.detect = function(obj, predicate, context) {
    var key;
    if (isArrayLike(obj)) {
      key = _.findIndex(obj, predicate, context);
    } else {
      key = _.findKey(obj, predicate, context);
    }
    if (key !== void 0 && key !== -1) return obj[key];
  };

  // Return all the elements that pass a truth test.
  // Aliased as `select`.
  _.filter = _.select = function(obj, predicate, context) {
    var results = [];
    predicate = cb(predicate, context);
    _.each(obj, function(value, index, list) {
      if (predicate(value, index, list)) results.push(value);
    });
    return results;
  };

  // Return all the elements for which a truth test fails.
  _.reject = function(obj, predicate, context) {
    return _.filter(obj, _.negate(cb(predicate)), context);
  };

  // Determine whether all of the elements match a truth test.
  // Aliased as `all`.
  _.every = _.all = function(obj, predicate, context) {
    predicate = cb(predicate, context);
    var keys = !isArrayLike(obj) && _.keys(obj),
        length = (keys || obj).length;
    for (var index = 0; index < length; index++) {
      var currentKey = keys ? keys[index] : index;
      if (!predicate(obj[currentKey], currentKey, obj)) return false;
    }
    return true;
  };

  // Determine if at least one element in the object matches a truth test.
  // Aliased as `any`.
  _.some = _.any = function(obj, predicate, context) {
    predicate = cb(predicate, context);
    var keys = !isArrayLike(obj) && _.keys(obj),
        length = (keys || obj).length;
    for (var index = 0; index < length; index++) {
      var currentKey = keys ? keys[index] : index;
      if (predicate(obj[currentKey], currentKey, obj)) return true;
    }
    return false;
  };

  // Determine if the array or object contains a given item (using `===`).
  // Aliased as `includes` and `include`.
  _.contains = _.includes = _.include = function(obj, item, fromIndex, guard) {
    if (!isArrayLike(obj)) obj = _.values(obj);
    if (typeof fromIndex != 'number' || guard) fromIndex = 0;
    return _.indexOf(obj, item, fromIndex) >= 0;
  };

  // Invoke a method (with arguments) on every item in a collection.
  _.invoke = function(obj, method) {
    var args = slice.call(arguments, 2);
    var isFunc = _.isFunction(method);
    return _.map(obj, function(value) {
      var func = isFunc ? method : value[method];
      return func == null ? func : func.apply(value, args);
    });
  };

  // Convenience version of a common use case of `map`: fetching a property.
  _.pluck = function(obj, key) {
    return _.map(obj, _.property(key));
  };

  // Convenience version of a common use case of `filter`: selecting only objects
  // containing specific `key:value` pairs.
  _.where = function(obj, attrs) {
    return _.filter(obj, _.matcher(attrs));
  };

  // Convenience version of a common use case of `find`: getting the first object
  // containing specific `key:value` pairs.
  _.findWhere = function(obj, attrs) {
    return _.find(obj, _.matcher(attrs));
  };

  // Return the maximum element (or element-based computation).
  _.max = function(obj, iteratee, context) {
    var result = -Infinity, lastComputed = -Infinity,
        value, computed;
    if (iteratee == null && obj != null) {
      obj = isArrayLike(obj) ? obj : _.values(obj);
      for (var i = 0, length = obj.length; i < length; i++) {
        value = obj[i];
        if (value > result) {
          result = value;
        }
      }
    } else {
      iteratee = cb(iteratee, context);
      _.each(obj, function(value, index, list) {
        computed = iteratee(value, index, list);
        if (computed > lastComputed || computed === -Infinity && result === -Infinity) {
          result = value;
          lastComputed = computed;
        }
      });
    }
    return result;
  };

  // Return the minimum element (or element-based computation).
  _.min = function(obj, iteratee, context) {
    var result = Infinity, lastComputed = Infinity,
        value, computed;
    if (iteratee == null && obj != null) {
      obj = isArrayLike(obj) ? obj : _.values(obj);
      for (var i = 0, length = obj.length; i < length; i++) {
        value = obj[i];
        if (value < result) {
          result = value;
        }
      }
    } else {
      iteratee = cb(iteratee, context);
      _.each(obj, function(value, index, list) {
        computed = iteratee(value, index, list);
        if (computed < lastComputed || computed === Infinity && result === Infinity) {
          result = value;
          lastComputed = computed;
        }
      });
    }
    return result;
  };

  // Shuffle a collection, using the modern version of the
  // [Fisher-Yates shuffle](http://en.wikipedia.org/wiki/Fisher–Yates_shuffle).
  _.shuffle = function(obj) {
    var set = isArrayLike(obj) ? obj : _.values(obj);
    var length = set.length;
    var shuffled = Array(length);
    for (var index = 0, rand; index < length; index++) {
      rand = _.random(0, index);
      if (rand !== index) shuffled[index] = shuffled[rand];
      shuffled[rand] = set[index];
    }
    return shuffled;
  };

  // Sample **n** random values from a collection.
  // If **n** is not specified, returns a single random element.
  // The internal `guard` argument allows it to work with `map`.
  _.sample = function(obj, n, guard) {
    if (n == null || guard) {
      if (!isArrayLike(obj)) obj = _.values(obj);
      return obj[_.random(obj.length - 1)];
    }
    return _.shuffle(obj).slice(0, Math.max(0, n));
  };

  // Sort the object's values by a criterion produced by an iteratee.
  _.sortBy = function(obj, iteratee, context) {
    iteratee = cb(iteratee, context);
    return _.pluck(_.map(obj, function(value, index, list) {
      return {
        value: value,
        index: index,
        criteria: iteratee(value, index, list)
      };
    }).sort(function(left, right) {
      var a = left.criteria;
      var b = right.criteria;
      if (a !== b) {
        if (a > b || a === void 0) return 1;
        if (a < b || b === void 0) return -1;
      }
      return left.index - right.index;
    }), 'value');
  };

  // An internal function used for aggregate "group by" operations.
  var group = function(behavior) {
    return function(obj, iteratee, context) {
      var result = {};
      iteratee = cb(iteratee, context);
      _.each(obj, function(value, index) {
        var key = iteratee(value, index, obj);
        behavior(result, value, key);
      });
      return result;
    };
  };

  // Groups the object's values by a criterion. Pass either a string attribute
  // to group by, or a function that returns the criterion.
  _.groupBy = group(function(result, value, key) {
    if (_.has(result, key)) result[key].push(value); else result[key] = [value];
  });

  // Indexes the object's values by a criterion, similar to `groupBy`, but for
  // when you know that your index values will be unique.
  _.indexBy = group(function(result, value, key) {
    result[key] = value;
  });

  // Counts instances of an object that group by a certain criterion. Pass
  // either a string attribute to count by, or a function that returns the
  // criterion.
  _.countBy = group(function(result, value, key) {
    if (_.has(result, key)) result[key]++; else result[key] = 1;
  });

  // Safely create a real, live array from anything iterable.
  _.toArray = function(obj) {
    if (!obj) return [];
    if (_.isArray(obj)) return slice.call(obj);
    if (isArrayLike(obj)) return _.map(obj, _.identity);
    return _.values(obj);
  };

  // Return the number of elements in an object.
  _.size = function(obj) {
    if (obj == null) return 0;
    return isArrayLike(obj) ? obj.length : _.keys(obj).length;
  };

  // Split a collection into two arrays: one whose elements all satisfy the given
  // predicate, and one whose elements all do not satisfy the predicate.
  _.partition = function(obj, predicate, context) {
    predicate = cb(predicate, context);
    var pass = [], fail = [];
    _.each(obj, function(value, key, obj) {
      (predicate(value, key, obj) ? pass : fail).push(value);
    });
    return [pass, fail];
  };

  // Array Functions
  // ---------------

  // Get the first element of an array. Passing **n** will return the first N
  // values in the array. Aliased as `head` and `take`. The **guard** check
  // allows it to work with `_.map`.
  _.first = _.head = _.take = function(array, n, guard) {
    if (array == null) return void 0;
    if (n == null || guard) return array[0];
    return _.initial(array, array.length - n);
  };

  // Returns everything but the last entry of the array. Especially useful on
  // the arguments object. Passing **n** will return all the values in
  // the array, excluding the last N.
  _.initial = function(array, n, guard) {
    return slice.call(array, 0, Math.max(0, array.length - (n == null || guard ? 1 : n)));
  };

  // Get the last element of an array. Passing **n** will return the last N
  // values in the array.
  _.last = function(array, n, guard) {
    if (array == null) return void 0;
    if (n == null || guard) return array[array.length - 1];
    return _.rest(array, Math.max(0, array.length - n));
  };

  // Returns everything but the first entry of the array. Aliased as `tail` and `drop`.
  // Especially useful on the arguments object. Passing an **n** will return
  // the rest N values in the array.
  _.rest = _.tail = _.drop = function(array, n, guard) {
    return slice.call(array, n == null || guard ? 1 : n);
  };

  // Trim out all falsy values from an array.
  _.compact = function(array) {
    return _.filter(array, _.identity);
  };

  // Internal implementation of a recursive `flatten` function.
  var flatten = function(input, shallow, strict, startIndex) {
    var output = [], idx = 0;
    for (var i = startIndex || 0, length = getLength(input); i < length; i++) {
      var value = input[i];
      if (isArrayLike(value) && (_.isArray(value) || _.isArguments(value))) {
        //flatten current level of array or arguments object
        if (!shallow) value = flatten(value, shallow, strict);
        var j = 0, len = value.length;
        output.length += len;
        while (j < len) {
          output[idx++] = value[j++];
        }
      } else if (!strict) {
        output[idx++] = value;
      }
    }
    return output;
  };

  // Flatten out an array, either recursively (by default), or just one level.
  _.flatten = function(array, shallow) {
    return flatten(array, shallow, false);
  };

  // Return a version of the array that does not contain the specified value(s).
  _.without = function(array) {
    return _.difference(array, slice.call(arguments, 1));
  };

  // Produce a duplicate-free version of the array. If the array has already
  // been sorted, you have the option of using a faster algorithm.
  // Aliased as `unique`.
  _.uniq = _.unique = function(array, isSorted, iteratee, context) {
    if (!_.isBoolean(isSorted)) {
      context = iteratee;
      iteratee = isSorted;
      isSorted = false;
    }
    if (iteratee != null) iteratee = cb(iteratee, context);
    var result = [];
    var seen = [];
    for (var i = 0, length = getLength(array); i < length; i++) {
      var value = array[i],
          computed = iteratee ? iteratee(value, i, array) : value;
      if (isSorted) {
        if (!i || seen !== computed) result.push(value);
        seen = computed;
      } else if (iteratee) {
        if (!_.contains(seen, computed)) {
          seen.push(computed);
          result.push(value);
        }
      } else if (!_.contains(result, value)) {
        result.push(value);
      }
    }
    return result;
  };

  // Produce an array that contains the union: each distinct element from all of
  // the passed-in arrays.
  _.union = function() {
    return _.uniq(flatten(arguments, true, true));
  };

  // Produce an array that contains every item shared between all the
  // passed-in arrays.
  _.intersection = function(array) {
    var result = [];
    var argsLength = arguments.length;
    for (var i = 0, length = getLength(array); i < length; i++) {
      var item = array[i];
      if (_.contains(result, item)) continue;
      for (var j = 1; j < argsLength; j++) {
        if (!_.contains(arguments[j], item)) break;
      }
      if (j === argsLength) result.push(item);
    }
    return result;
  };

  // Take the difference between one array and a number of other arrays.
  // Only the elements present in just the first array will remain.
  _.difference = function(array) {
    var rest = flatten(arguments, true, true, 1);
    return _.filter(array, function(value){
      return !_.contains(rest, value);
    });
  };

  // Zip together multiple lists into a single array -- elements that share
  // an index go together.
  _.zip = function() {
    return _.unzip(arguments);
  };

  // Complement of _.zip. Unzip accepts an array of arrays and groups
  // each array's elements on shared indices
  _.unzip = function(array) {
    var length = array && _.max(array, getLength).length || 0;
    var result = Array(length);

    for (var index = 0; index < length; index++) {
      result[index] = _.pluck(array, index);
    }
    return result;
  };

  // Converts lists into objects. Pass either a single array of `[key, value]`
  // pairs, or two parallel arrays of the same length -- one of keys, and one of
  // the corresponding values.
  _.object = function(list, values) {
    var result = {};
    for (var i = 0, length = getLength(list); i < length; i++) {
      if (values) {
        result[list[i]] = values[i];
      } else {
        result[list[i][0]] = list[i][1];
      }
    }
    return result;
  };

  // Generator function to create the findIndex and findLastIndex functions
  function createPredicateIndexFinder(dir) {
    return function(array, predicate, context) {
      predicate = cb(predicate, context);
      var length = getLength(array);
      var index = dir > 0 ? 0 : length - 1;
      for (; index >= 0 && index < length; index += dir) {
        if (predicate(array[index], index, array)) return index;
      }
      return -1;
    };
  }

  // Returns the first index on an array-like that passes a predicate test
  _.findIndex = createPredicateIndexFinder(1);
  _.findLastIndex = createPredicateIndexFinder(-1);

  // Use a comparator function to figure out the smallest index at which
  // an object should be inserted so as to maintain order. Uses binary search.
  _.sortedIndex = function(array, obj, iteratee, context) {
    iteratee = cb(iteratee, context, 1);
    var value = iteratee(obj);
    var low = 0, high = getLength(array);
    while (low < high) {
      var mid = Math.floor((low + high) / 2);
      if (iteratee(array[mid]) < value) low = mid + 1; else high = mid;
    }
    return low;
  };

  // Generator function to create the indexOf and lastIndexOf functions
  function createIndexFinder(dir, predicateFind, sortedIndex) {
    return function(array, item, idx) {
      var i = 0, length = getLength(array);
      if (typeof idx == 'number') {
        if (dir > 0) {
            i = idx >= 0 ? idx : Math.max(idx + length, i);
        } else {
            length = idx >= 0 ? Math.min(idx + 1, length) : idx + length + 1;
        }
      } else if (sortedIndex && idx && length) {
        idx = sortedIndex(array, item);
        return array[idx] === item ? idx : -1;
      }
      if (item !== item) {
        idx = predicateFind(slice.call(array, i, length), _.isNaN);
        return idx >= 0 ? idx + i : -1;
      }
      for (idx = dir > 0 ? i : length - 1; idx >= 0 && idx < length; idx += dir) {
        if (array[idx] === item) return idx;
      }
      return -1;
    };
  }

  // Return the position of the first occurrence of an item in an array,
  // or -1 if the item is not included in the array.
  // If the array is large and already in sort order, pass `true`
  // for **isSorted** to use binary search.
  _.indexOf = createIndexFinder(1, _.findIndex, _.sortedIndex);
  _.lastIndexOf = createIndexFinder(-1, _.findLastIndex);

  // Generate an integer Array containing an arithmetic progression. A port of
  // the native Python `range()` function. See
  // [the Python documentation](http://docs.python.org/library/functions.html#range).
  _.range = function(start, stop, step) {
    if (stop == null) {
      stop = start || 0;
      start = 0;
    }
    step = step || 1;

    var length = Math.max(Math.ceil((stop - start) / step), 0);
    var range = Array(length);

    for (var idx = 0; idx < length; idx++, start += step) {
      range[idx] = start;
    }

    return range;
  };

  // Function (ahem) Functions
  // ------------------

  // Determines whether to execute a function as a constructor
  // or a normal function with the provided arguments
  var executeBound = function(sourceFunc, boundFunc, context, callingContext, args) {
    if (!(callingContext instanceof boundFunc)) return sourceFunc.apply(context, args);
    var self = baseCreate(sourceFunc.prototype);
    var result = sourceFunc.apply(self, args);
    if (_.isObject(result)) return result;
    return self;
  };

  // Create a function bound to a given object (assigning `this`, and arguments,
  // optionally). Delegates to **ECMAScript 5**'s native `Function.bind` if
  // available.
  _.bind = function(func, context) {
    if (nativeBind && func.bind === nativeBind) return nativeBind.apply(func, slice.call(arguments, 1));
    if (!_.isFunction(func)) throw new TypeError('Bind must be called on a function');
    var args = slice.call(arguments, 2);
    var bound = function() {
      return executeBound(func, bound, context, this, args.concat(slice.call(arguments)));
    };
    return bound;
  };

  // Partially apply a function by creating a version that has had some of its
  // arguments pre-filled, without changing its dynamic `this` context. _ acts
  // as a placeholder, allowing any combination of arguments to be pre-filled.
  _.partial = function(func) {
    var boundArgs = slice.call(arguments, 1);
    var bound = function() {
      var position = 0, length = boundArgs.length;
      var args = Array(length);
      for (var i = 0; i < length; i++) {
        args[i] = boundArgs[i] === _ ? arguments[position++] : boundArgs[i];
      }
      while (position < arguments.length) args.push(arguments[position++]);
      return executeBound(func, bound, this, this, args);
    };
    return bound;
  };

  // Bind a number of an object's methods to that object. Remaining arguments
  // are the method names to be bound. Useful for ensuring that all callbacks
  // defined on an object belong to it.
  _.bindAll = function(obj) {
    var i, length = arguments.length, key;
    if (length <= 1) throw new Error('bindAll must be passed function names');
    for (i = 1; i < length; i++) {
      key = arguments[i];
      obj[key] = _.bind(obj[key], obj);
    }
    return obj;
  };

  // Memoize an expensive function by storing its results.
  _.memoize = function(func, hasher) {
    var memoize = function(key) {
      var cache = memoize.cache;
      var address = '' + (hasher ? hasher.apply(this, arguments) : key);
      if (!_.has(cache, address)) cache[address] = func.apply(this, arguments);
      return cache[address];
    };
    memoize.cache = {};
    return memoize;
  };

  // Delays a function for the given number of milliseconds, and then calls
  // it with the arguments supplied.
  _.delay = function(func, wait) {
    var args = slice.call(arguments, 2);
    return setTimeout(function(){
      return func.apply(null, args);
    }, wait);
  };

  // Defers a function, scheduling it to run after the current call stack has
  // cleared.
  _.defer = _.partial(_.delay, _, 1);

  // Returns a function, that, when invoked, will only be triggered at most once
  // during a given window of time. Normally, the throttled function will run
  // as much as it can, without ever going more than once per `wait` duration;
  // but if you'd like to disable the execution on the leading edge, pass
  // `{leading: false}`. To disable execution on the trailing edge, ditto.
  _.throttle = function(func, wait, options) {
    var context, args, result;
    var timeout = null;
    var previous = 0;
    if (!options) options = {};
    var later = function() {
      previous = options.leading === false ? 0 : _.now();
      timeout = null;
      result = func.apply(context, args);
      if (!timeout) context = args = null;
    };
    return function() {
      var now = _.now();
      if (!previous && options.leading === false) previous = now;
      var remaining = wait - (now - previous);
      context = this;
      args = arguments;
      if (remaining <= 0 || remaining > wait) {
        if (timeout) {
          clearTimeout(timeout);
          timeout = null;
        }
        previous = now;
        result = func.apply(context, args);
        if (!timeout) context = args = null;
      } else if (!timeout && options.trailing !== false) {
        timeout = setTimeout(later, remaining);
      }
      return result;
    };
  };

  // Returns a function, that, as long as it continues to be invoked, will not
  // be triggered. The function will be called after it stops being called for
  // N milliseconds. If `immediate` is passed, trigger the function on the
  // leading edge, instead of the trailing.
  _.debounce = function(func, wait, immediate) {
    var timeout, args, context, timestamp, result;

    var later = function() {
      var last = _.now() - timestamp;

      if (last < wait && last >= 0) {
        timeout = setTimeout(later, wait - last);
      } else {
        timeout = null;
        if (!immediate) {
          result = func.apply(context, args);
          if (!timeout) context = args = null;
        }
      }
    };

    return function() {
      context = this;
      args = arguments;
      timestamp = _.now();
      var callNow = immediate && !timeout;
      if (!timeout) timeout = setTimeout(later, wait);
      if (callNow) {
        result = func.apply(context, args);
        context = args = null;
      }

      return result;
    };
  };

  // Returns the first function passed as an argument to the second,
  // allowing you to adjust arguments, run code before and after, and
  // conditionally execute the original function.
  _.wrap = function(func, wrapper) {
    return _.partial(wrapper, func);
  };

  // Returns a negated version of the passed-in predicate.
  _.negate = function(predicate) {
    return function() {
      return !predicate.apply(this, arguments);
    };
  };

  // Returns a function that is the composition of a list of functions, each
  // consuming the return value of the function that follows.
  _.compose = function() {
    var args = arguments;
    var start = args.length - 1;
    return function() {
      var i = start;
      var result = args[start].apply(this, arguments);
      while (i--) result = args[i].call(this, result);
      return result;
    };
  };

  // Returns a function that will only be executed on and after the Nth call.
  _.after = function(times, func) {
    return function() {
      if (--times < 1) {
        return func.apply(this, arguments);
      }
    };
  };

  // Returns a function that will only be executed up to (but not including) the Nth call.
  _.before = function(times, func) {
    var memo;
    return function() {
      if (--times > 0) {
        memo = func.apply(this, arguments);
      }
      if (times <= 1) func = null;
      return memo;
    };
  };

  // Returns a function that will be executed at most one time, no matter how
  // often you call it. Useful for lazy initialization.
  _.once = _.partial(_.before, 2);

  // Object Functions
  // ----------------

  // Keys in IE < 9 that won't be iterated by `for key in ...` and thus missed.
  var hasEnumBug = !{toString: null}.propertyIsEnumerable('toString');
  var nonEnumerableProps = ['valueOf', 'isPrototypeOf', 'toString',
                      'propertyIsEnumerable', 'hasOwnProperty', 'toLocaleString'];

  function collectNonEnumProps(obj, keys) {
    var nonEnumIdx = nonEnumerableProps.length;
    var constructor = obj.constructor;
    var proto = (_.isFunction(constructor) && constructor.prototype) || ObjProto;

    // Constructor is a special case.
    var prop = 'constructor';
    if (_.has(obj, prop) && !_.contains(keys, prop)) keys.push(prop);

    while (nonEnumIdx--) {
      prop = nonEnumerableProps[nonEnumIdx];
      if (prop in obj && obj[prop] !== proto[prop] && !_.contains(keys, prop)) {
        keys.push(prop);
      }
    }
  }

  // Retrieve the names of an object's own properties.
  // Delegates to **ECMAScript 5**'s native `Object.keys`
  _.keys = function(obj) {
    if (!_.isObject(obj)) return [];
    if (nativeKeys) return nativeKeys(obj);
    var keys = [];
    for (var key in obj) if (_.has(obj, key)) keys.push(key);
    // Ahem, IE < 9.
    if (hasEnumBug) collectNonEnumProps(obj, keys);
    return keys;
  };

  // Retrieve all the property names of an object.
  _.allKeys = function(obj) {
    if (!_.isObject(obj)) return [];
    var keys = [];
    for (var key in obj) keys.push(key);
    // Ahem, IE < 9.
    if (hasEnumBug) collectNonEnumProps(obj, keys);
    return keys;
  };

  // Retrieve the values of an object's properties.
  _.values = function(obj) {
    var keys = _.keys(obj);
    var length = keys.length;
    var values = Array(length);
    for (var i = 0; i < length; i++) {
      values[i] = obj[keys[i]];
    }
    return values;
  };

  // Returns the results of applying the iteratee to each element of the object
  // In contrast to _.map it returns an object
  _.mapObject = function(obj, iteratee, context) {
    iteratee = cb(iteratee, context);
    var keys =  _.keys(obj),
          length = keys.length,
          results = {},
          currentKey;
      for (var index = 0; index < length; index++) {
        currentKey = keys[index];
        results[currentKey] = iteratee(obj[currentKey], currentKey, obj);
      }
      return results;
  };

  // Convert an object into a list of `[key, value]` pairs.
  _.pairs = function(obj) {
    var keys = _.keys(obj);
    var length = keys.length;
    var pairs = Array(length);
    for (var i = 0; i < length; i++) {
      pairs[i] = [keys[i], obj[keys[i]]];
    }
    return pairs;
  };

  // Invert the keys and values of an object. The values must be serializable.
  _.invert = function(obj) {
    var result = {};
    var keys = _.keys(obj);
    for (var i = 0, length = keys.length; i < length; i++) {
      result[obj[keys[i]]] = keys[i];
    }
    return result;
  };

  // Return a sorted list of the function names available on the object.
  // Aliased as `methods`
  _.functions = _.methods = function(obj) {
    var names = [];
    for (var key in obj) {
      if (_.isFunction(obj[key])) names.push(key);
    }
    return names.sort();
  };

  // Extend a given object with all the properties in passed-in object(s).
  _.extend = createAssigner(_.allKeys);

  // Assigns a given object with all the own properties in the passed-in object(s)
  // (https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)
  _.extendOwn = _.assign = createAssigner(_.keys);

  // Returns the first key on an object that passes a predicate test
  _.findKey = function(obj, predicate, context) {
    predicate = cb(predicate, context);
    var keys = _.keys(obj), key;
    for (var i = 0, length = keys.length; i < length; i++) {
      key = keys[i];
      if (predicate(obj[key], key, obj)) return key;
    }
  };

  // Return a copy of the object only containing the whitelisted properties.
  _.pick = function(object, oiteratee, context) {
    var result = {}, obj = object, iteratee, keys;
    if (obj == null) return result;
    if (_.isFunction(oiteratee)) {
      keys = _.allKeys(obj);
      iteratee = optimizeCb(oiteratee, context);
    } else {
      keys = flatten(arguments, false, false, 1);
      iteratee = function(value, key, obj) { return key in obj; };
      obj = Object(obj);
    }
    for (var i = 0, length = keys.length; i < length; i++) {
      var key = keys[i];
      var value = obj[key];
      if (iteratee(value, key, obj)) result[key] = value;
    }
    return result;
  };

   // Return a copy of the object without the blacklisted properties.
  _.omit = function(obj, iteratee, context) {
    if (_.isFunction(iteratee)) {
      iteratee = _.negate(iteratee);
    } else {
      var keys = _.map(flatten(arguments, false, false, 1), String);
      iteratee = function(value, key) {
        return !_.contains(keys, key);
      };
    }
    return _.pick(obj, iteratee, context);
  };

  // Fill in a given object with default properties.
  _.defaults = createAssigner(_.allKeys, true);

  // Creates an object that inherits from the given prototype object.
  // If additional properties are provided then they will be added to the
  // created object.
  _.create = function(prototype, props) {
    var result = baseCreate(prototype);
    if (props) _.extendOwn(result, props);
    return result;
  };

  // Create a (shallow-cloned) duplicate of an object.
  _.clone = function(obj) {
    if (!_.isObject(obj)) return obj;
    return _.isArray(obj) ? obj.slice() : _.extend({}, obj);
  };

  // Invokes interceptor with the obj, and then returns obj.
  // The primary purpose of this method is to "tap into" a method chain, in
  // order to perform operations on intermediate results within the chain.
  _.tap = function(obj, interceptor) {
    interceptor(obj);
    return obj;
  };

  // Returns whether an object has a given set of `key:value` pairs.
  _.isMatch = function(object, attrs) {
    var keys = _.keys(attrs), length = keys.length;
    if (object == null) return !length;
    var obj = Object(object);
    for (var i = 0; i < length; i++) {
      var key = keys[i];
      if (attrs[key] !== obj[key] || !(key in obj)) return false;
    }
    return true;
  };


  // Internal recursive comparison function for `isEqual`.
  var eq = function(a, b, aStack, bStack) {
    // Identical objects are equal. `0 === -0`, but they aren't identical.
    // See the [Harmony `egal` proposal](http://wiki.ecmascript.org/doku.php?id=harmony:egal).
    if (a === b) return a !== 0 || 1 / a === 1 / b;
    // A strict comparison is necessary because `null == undefined`.
    if (a == null || b == null) return a === b;
    // Unwrap any wrapped objects.
    if (a instanceof _) a = a._wrapped;
    if (b instanceof _) b = b._wrapped;
    // Compare `[[Class]]` names.
    var className = toString.call(a);
    if (className !== toString.call(b)) return false;
    switch (className) {
      // Strings, numbers, regular expressions, dates, and booleans are compared by value.
      case '[object RegExp]':
      // RegExps are coerced to strings for comparison (Note: '' + /a/i === '/a/i')
      case '[object String]':
        // Primitives and their corresponding object wrappers are equivalent; thus, `"5"` is
        // equivalent to `new String("5")`.
        return '' + a === '' + b;
      case '[object Number]':
        // `NaN`s are equivalent, but non-reflexive.
        // Object(NaN) is equivalent to NaN
        if (+a !== +a) return +b !== +b;
        // An `egal` comparison is performed for other numeric values.
        return +a === 0 ? 1 / +a === 1 / b : +a === +b;
      case '[object Date]':
      case '[object Boolean]':
        // Coerce dates and booleans to numeric primitive values. Dates are compared by their
        // millisecond representations. Note that invalid dates with millisecond representations
        // of `NaN` are not equivalent.
        return +a === +b;
    }

    var areArrays = className === '[object Array]';
    if (!areArrays) {
      if (typeof a != 'object' || typeof b != 'object') return false;

      // Objects with different constructors are not equivalent, but `Object`s or `Array`s
      // from different frames are.
      var aCtor = a.constructor, bCtor = b.constructor;
      if (aCtor !== bCtor && !(_.isFunction(aCtor) && aCtor instanceof aCtor &&
                               _.isFunction(bCtor) && bCtor instanceof bCtor)
                          && ('constructor' in a && 'constructor' in b)) {
        return false;
      }
    }
    // Assume equality for cyclic structures. The algorithm for detecting cyclic
    // structures is adapted from ES 5.1 section 15.12.3, abstract operation `JO`.

    // Initializing stack of traversed objects.
    // It's done here since we only need them for objects and arrays comparison.
    aStack = aStack || [];
    bStack = bStack || [];
    var length = aStack.length;
    while (length--) {
      // Linear search. Performance is inversely proportional to the number of
      // unique nested structures.
      if (aStack[length] === a) return bStack[length] === b;
    }

    // Add the first object to the stack of traversed objects.
    aStack.push(a);
    bStack.push(b);

    // Recursively compare objects and arrays.
    if (areArrays) {
      // Compare array lengths to determine if a deep comparison is necessary.
      length = a.length;
      if (length !== b.length) return false;
      // Deep compare the contents, ignoring non-numeric properties.
      while (length--) {
        if (!eq(a[length], b[length], aStack, bStack)) return false;
      }
    } else {
      // Deep compare objects.
      var keys = _.keys(a), key;
      length = keys.length;
      // Ensure that both objects contain the same number of properties before comparing deep equality.
      if (_.keys(b).length !== length) return false;
      while (length--) {
        // Deep compare each member
        key = keys[length];
        if (!(_.has(b, key) && eq(a[key], b[key], aStack, bStack))) return false;
      }
    }
    // Remove the first object from the stack of traversed objects.
    aStack.pop();
    bStack.pop();
    return true;
  };

  // Perform a deep comparison to check if two objects are equal.
  _.isEqual = function(a, b) {
    return eq(a, b);
  };

  // Is a given array, string, or object empty?
  // An "empty" object has no enumerable own-properties.
  _.isEmpty = function(obj) {
    if (obj == null) return true;
    if (isArrayLike(obj) && (_.isArray(obj) || _.isString(obj) || _.isArguments(obj))) return obj.length === 0;
    return _.keys(obj).length === 0;
  };

  // Is a given value a DOM element?
  _.isElement = function(obj) {
    return !!(obj && obj.nodeType === 1);
  };

  // Is a given value an array?
  // Delegates to ECMA5's native Array.isArray
  _.isArray = nativeIsArray || function(obj) {
    return toString.call(obj) === '[object Array]';
  };

  // Is a given variable an object?
  _.isObject = function(obj) {
    var type = typeof obj;
    return type === 'function' || type === 'object' && !!obj;
  };

  // Add some isType methods: isArguments, isFunction, isString, isNumber, isDate, isRegExp, isError.
  _.each(['Arguments', 'Function', 'String', 'Number', 'Date', 'RegExp', 'Error'], function(name) {
    _['is' + name] = function(obj) {
      return toString.call(obj) === '[object ' + name + ']';
    };
  });

  // Define a fallback version of the method in browsers (ahem, IE < 9), where
  // there isn't any inspectable "Arguments" type.
  if (!_.isArguments(arguments)) {
    _.isArguments = function(obj) {
      return _.has(obj, 'callee');
    };
  }

  // Optimize `isFunction` if appropriate. Work around some typeof bugs in old v8,
  // IE 11 (#1621), and in Safari 8 (#1929).
  if (typeof /./ != 'function' && typeof Int8Array != 'object') {
    _.isFunction = function(obj) {
      return typeof obj == 'function' || false;
    };
  }

  // Is a given object a finite number?
  _.isFinite = function(obj) {
    return isFinite(obj) && !isNaN(parseFloat(obj));
  };

  // Is the given value `NaN`? (NaN is the only number which does not equal itself).
  _.isNaN = function(obj) {
    return _.isNumber(obj) && obj !== +obj;
  };

  // Is a given value a boolean?
  _.isBoolean = function(obj) {
    return obj === true || obj === false || toString.call(obj) === '[object Boolean]';
  };

  // Is a given value equal to null?
  _.isNull = function(obj) {
    return obj === null;
  };

  // Is a given variable undefined?
  _.isUndefined = function(obj) {
    return obj === void 0;
  };

  // Shortcut function for checking if an object has a given property directly
  // on itself (in other words, not on a prototype).
  _.has = function(obj, key) {
    return obj != null && hasOwnProperty.call(obj, key);
  };

  // Utility Functions
  // -----------------

  // Run Underscore.js in *noConflict* mode, returning the `_` variable to its
  // previous owner. Returns a reference to the Underscore object.
  _.noConflict = function() {
    root._ = previousUnderscore;
    return this;
  };

  // Keep the identity function around for default iteratees.
  _.identity = function(value) {
    return value;
  };

  // Predicate-generating functions. Often useful outside of Underscore.
  _.constant = function(value) {
    return function() {
      return value;
    };
  };

  _.noop = function(){};

  _.property = property;

  // Generates a function for a given object that returns a given property.
  _.propertyOf = function(obj) {
    return obj == null ? function(){} : function(key) {
      return obj[key];
    };
  };

  // Returns a predicate for checking whether an object has a given set of
  // `key:value` pairs.
  _.matcher = _.matches = function(attrs) {
    attrs = _.extendOwn({}, attrs);
    return function(obj) {
      return _.isMatch(obj, attrs);
    };
  };

  // Run a function **n** times.
  _.times = function(n, iteratee, context) {
    var accum = Array(Math.max(0, n));
    iteratee = optimizeCb(iteratee, context, 1);
    for (var i = 0; i < n; i++) accum[i] = iteratee(i);
    return accum;
  };

  // Return a random integer between min and max (inclusive).
  _.random = function(min, max) {
    if (max == null) {
      max = min;
      min = 0;
    }
    return min + Math.floor(Math.random() * (max - min + 1));
  };

  // A (possibly faster) way to get the current timestamp as an integer.
  _.now = Date.now || function() {
    return new Date().getTime();
  };

   // List of HTML entities for escaping.
  var escapeMap = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#x27;',
    '`': '&#x60;'
  };
  var unescapeMap = _.invert(escapeMap);

  // Functions for escaping and unescaping strings to/from HTML interpolation.
  var createEscaper = function(map) {
    var escaper = function(match) {
      return map[match];
    };
    // Regexes for identifying a key that needs to be escaped
    var source = '(?:' + _.keys(map).join('|') + ')';
    var testRegexp = RegExp(source);
    var replaceRegexp = RegExp(source, 'g');
    return function(string) {
      string = string == null ? '' : '' + string;
      return testRegexp.test(string) ? string.replace(replaceRegexp, escaper) : string;
    };
  };
  _.escape = createEscaper(escapeMap);
  _.unescape = createEscaper(unescapeMap);

  // If the value of the named `property` is a function then invoke it with the
  // `object` as context; otherwise, return it.
  _.result = function(object, property, fallback) {
    var value = object == null ? void 0 : object[property];
    if (value === void 0) {
      value = fallback;
    }
    return _.isFunction(value) ? value.call(object) : value;
  };

  // Generate a unique integer id (unique within the entire client session).
  // Useful for temporary DOM ids.
  var idCounter = 0;
  _.uniqueId = function(prefix) {
    var id = ++idCounter + '';
    return prefix ? prefix + id : id;
  };

  // By default, Underscore uses ERB-style template delimiters, change the
  // following template settings to use alternative delimiters.
  _.templateSettings = {
    evaluate    : /<%([\s\S]+?)%>/g,
    interpolate : /<%=([\s\S]+?)%>/g,
    escape      : /<%-([\s\S]+?)%>/g
  };

  // When customizing `templateSettings`, if you don't want to define an
  // interpolation, evaluation or escaping regex, we need one that is
  // guaranteed not to match.
  var noMatch = /(.)^/;

  // Certain characters need to be escaped so that they can be put into a
  // string literal.
  var escapes = {
    "'":      "'",
    '\\':     '\\',
    '\r':     'r',
    '\n':     'n',
    '\u2028': 'u2028',
    '\u2029': 'u2029'
  };

  var escaper = /\\|'|\r|\n|\u2028|\u2029/g;

  var escapeChar = function(match) {
    return '\\' + escapes[match];
  };

  // JavaScript micro-templating, similar to John Resig's implementation.
  // Underscore templating handles arbitrary delimiters, preserves whitespace,
  // and correctly escapes quotes within interpolated code.
  // NB: `oldSettings` only exists for backwards compatibility.
  _.template = function(text, settings, oldSettings) {
    if (!settings && oldSettings) settings = oldSettings;
    settings = _.defaults({}, settings, _.templateSettings);

    // Combine delimiters into one regular expression via alternation.
    var matcher = RegExp([
      (settings.escape || noMatch).source,
      (settings.interpolate || noMatch).source,
      (settings.evaluate || noMatch).source
    ].join('|') + '|$', 'g');

    // Compile the template source, escaping string literals appropriately.
    var index = 0;
    var source = "__p+='";
    text.replace(matcher, function(match, escape, interpolate, evaluate, offset) {
      source += text.slice(index, offset).replace(escaper, escapeChar);
      index = offset + match.length;

      if (escape) {
        source += "'+\n((__t=(" + escape + "))==null?'':_.escape(__t))+\n'";
      } else if (interpolate) {
        source += "'+\n((__t=(" + interpolate + "))==null?'':__t)+\n'";
      } else if (evaluate) {
        source += "';\n" + evaluate + "\n__p+='";
      }

      // Adobe VMs need the match returned to produce the correct offest.
      return match;
    });
    source += "';\n";

    // If a variable is not specified, place data values in local scope.
    if (!settings.variable) source = 'with(obj||{}){\n' + source + '}\n';

    source = "var __t,__p='',__j=Array.prototype.join," +
      "print=function(){__p+=__j.call(arguments,'');};\n" +
      source + 'return __p;\n';

    try {
      var render = new Function(settings.variable || 'obj', '_', source);
    } catch (e) {
      e.source = source;
      throw e;
    }

    var template = function(data) {
      return render.call(this, data, _);
    };

    // Provide the compiled source as a convenience for precompilation.
    var argument = settings.variable || 'obj';
    template.source = 'function(' + argument + '){\n' + source + '}';

    return template;
  };

  // Add a "chain" function. Start chaining a wrapped Underscore object.
  _.chain = function(obj) {
    var instance = _(obj);
    instance._chain = true;
    return instance;
  };

  // OOP
  // ---------------
  // If Underscore is called as a function, it returns a wrapped object that
  // can be used OO-style. This wrapper holds altered versions of all the
  // underscore functions. Wrapped objects may be chained.

  // Helper function to continue chaining intermediate results.
  var result = function(instance, obj) {
    return instance._chain ? _(obj).chain() : obj;
  };

  // Add your own custom functions to the Underscore object.
  _.mixin = function(obj) {
    _.each(_.functions(obj), function(name) {
      var func = _[name] = obj[name];
      _.prototype[name] = function() {
        var args = [this._wrapped];
        push.apply(args, arguments);
        return result(this, func.apply(_, args));
      };
    });
  };

  // Add all of the Underscore functions to the wrapper object.
  _.mixin(_);

  // Add all mutator Array functions to the wrapper.
  _.each(['pop', 'push', 'reverse', 'shift', 'sort', 'splice', 'unshift'], function(name) {
    var method = ArrayProto[name];
    _.prototype[name] = function() {
      var obj = this._wrapped;
      method.apply(obj, arguments);
      if ((name === 'shift' || name === 'splice') && obj.length === 0) delete obj[0];
      return result(this, obj);
    };
  });

  // Add all accessor Array functions to the wrapper.
  _.each(['concat', 'join', 'slice'], function(name) {
    var method = ArrayProto[name];
    _.prototype[name] = function() {
      return result(this, method.apply(this._wrapped, arguments));
    };
  });

  // Extracts the result from a wrapped and chained object.
  _.prototype.value = function() {
    return this._wrapped;
  };

  // Provide unwrapping proxy for some methods used in engine operations
  // such as arithmetic and JSON stringification.
  _.prototype.valueOf = _.prototype.toJSON = _.prototype.value;

  _.prototype.toString = function() {
    return '' + this._wrapped;
  };

  // AMD registration happens at the end for compatibility with AMD loaders
  // that may not enforce next-turn semantics on modules. Even though general
  // practice for AMD registration is to be anonymous, underscore registers
  // as a named module because, like jQuery, it is a base library that is
  // popular enough to be bundled in a third party lib, but not be part of
  // an AMD load request. Those cases could generate an error when an
  // anonymous define() is called outside of a loader request.
  if (typeof define === 'function' && define.amd) {
    define('underscore', [], function() {
      return _;
    });
  }
}.call(this));
;/*
 AngularJS v1.5.11
 (c) 2010-2017 Google, Inc. http://angularjs.org
 License: MIT
*/
(function(y){'use strict';function G(a,b){b=b||Error;return function(){var d=arguments[0],c;c="["+(a?a+":":"")+d+"] http://errors.angularjs.org/1.5.11/"+(a?a+"/":"")+d;for(d=1;d<arguments.length;d++){c=c+(1==d?"?":"&")+"p"+(d-1)+"=";var f=encodeURIComponent,e;e=arguments[d];e="function"==typeof e?e.toString().replace(/ \{[\s\S]*$/,""):"undefined"==typeof e?"undefined":"string"!=typeof e?JSON.stringify(e):e;c+=f(e)}return new b(c)}}function la(a){if(null==a||Ya(a))return!1;if(I(a)||D(a)||F&&a instanceof
F)return!0;var b="length"in Object(a)&&a.length;return ba(b)&&(0<=b&&(b-1 in a||a instanceof Array)||"function"===typeof a.item)}function q(a,b,d){var c,f;if(a)if(C(a))for(c in a)"prototype"===c||"length"===c||"name"===c||a.hasOwnProperty&&!a.hasOwnProperty(c)||b.call(d,a[c],c,a);else if(I(a)||la(a)){var e="object"!==typeof a;c=0;for(f=a.length;c<f;c++)(e||c in a)&&b.call(d,a[c],c,a)}else if(a.forEach&&a.forEach!==q)a.forEach(b,d,a);else if(xc(a))for(c in a)b.call(d,a[c],c,a);else if("function"===
typeof a.hasOwnProperty)for(c in a)a.hasOwnProperty(c)&&b.call(d,a[c],c,a);else for(c in a)ua.call(a,c)&&b.call(d,a[c],c,a);return a}function yc(a,b,d){for(var c=Object.keys(a).sort(),f=0;f<c.length;f++)b.call(d,a[c[f]],c[f]);return c}function zc(a){return function(b,d){a(d,b)}}function ke(){return++sb}function Rb(a,b,d){for(var c=a.$$hashKey,f=0,e=b.length;f<e;++f){var g=b[f];if(E(g)||C(g))for(var h=Object.keys(g),k=0,l=h.length;k<l;k++){var m=h[k],n=g[m];d&&E(n)?ja(n)?a[m]=new Date(n.valueOf()):
Za(n)?a[m]=new RegExp(n):n.nodeName?a[m]=n.cloneNode(!0):Sb(n)?a[m]=n.clone():(E(a[m])||(a[m]=I(n)?[]:{}),Rb(a[m],[n],!0)):a[m]=n}}c?a.$$hashKey=c:delete a.$$hashKey;return a}function R(a){return Rb(a,va.call(arguments,1),!1)}function le(a){return Rb(a,va.call(arguments,1),!0)}function Z(a){return parseInt(a,10)}function Tb(a,b){return R(Object.create(a),b)}function w(){}function $a(a){return a}function ha(a){return function(){return a}}function Ac(a){return C(a.toString)&&a.toString!==ma}function z(a){return"undefined"===
typeof a}function x(a){return"undefined"!==typeof a}function E(a){return null!==a&&"object"===typeof a}function xc(a){return null!==a&&"object"===typeof a&&!Bc(a)}function D(a){return"string"===typeof a}function ba(a){return"number"===typeof a}function ja(a){return"[object Date]"===ma.call(a)}function C(a){return"function"===typeof a}function Za(a){return"[object RegExp]"===ma.call(a)}function Ya(a){return a&&a.window===a}function ab(a){return a&&a.$evalAsync&&a.$watch}function Ka(a){return"boolean"===
typeof a}function me(a){return a&&ba(a.length)&&ne.test(ma.call(a))}function Sb(a){return!(!a||!(a.nodeName||a.prop&&a.attr&&a.find))}function oe(a){var b={};a=a.split(",");var d;for(d=0;d<a.length;d++)b[a[d]]=!0;return b}function wa(a){return Q(a.nodeName||a[0]&&a[0].nodeName)}function bb(a,b){var d=a.indexOf(b);0<=d&&a.splice(d,1);return d}function sa(a,b){function d(a,b){var d=b.$$hashKey,e;if(I(a)){e=0;for(var f=a.length;e<f;e++)b.push(c(a[e]))}else if(xc(a))for(e in a)b[e]=c(a[e]);else if(a&&
"function"===typeof a.hasOwnProperty)for(e in a)a.hasOwnProperty(e)&&(b[e]=c(a[e]));else for(e in a)ua.call(a,e)&&(b[e]=c(a[e]));d?b.$$hashKey=d:delete b.$$hashKey;return b}function c(a){if(!E(a))return a;var b=e.indexOf(a);if(-1!==b)return g[b];if(Ya(a)||ab(a))throw xa("cpws");var b=!1,c=f(a);void 0===c&&(c=I(a)?[]:Object.create(Bc(a)),b=!0);e.push(a);g.push(c);return b?d(a,c):c}function f(a){switch(ma.call(a)){case "[object Int8Array]":case "[object Int16Array]":case "[object Int32Array]":case "[object Float32Array]":case "[object Float64Array]":case "[object Uint8Array]":case "[object Uint8ClampedArray]":case "[object Uint16Array]":case "[object Uint32Array]":return new a.constructor(c(a.buffer),
a.byteOffset,a.length);case "[object ArrayBuffer]":if(!a.slice){var b=new ArrayBuffer(a.byteLength);(new Uint8Array(b)).set(new Uint8Array(a));return b}return a.slice(0);case "[object Boolean]":case "[object Number]":case "[object String]":case "[object Date]":return new a.constructor(a.valueOf());case "[object RegExp]":return b=new RegExp(a.source,a.toString().match(/[^/]*$/)[0]),b.lastIndex=a.lastIndex,b;case "[object Blob]":return new a.constructor([a],{type:a.type})}if(C(a.cloneNode))return a.cloneNode(!0)}
var e=[],g=[];if(b){if(me(b)||"[object ArrayBuffer]"===ma.call(b))throw xa("cpta");if(a===b)throw xa("cpi");I(b)?b.length=0:q(b,function(a,d){"$$hashKey"!==d&&delete b[d]});e.push(a);g.push(b);return d(a,b)}return c(a)}function na(a,b){if(a===b)return!0;if(null===a||null===b)return!1;if(a!==a&&b!==b)return!0;var d=typeof a,c;if(d===typeof b&&"object"===d)if(I(a)){if(!I(b))return!1;if((d=a.length)===b.length){for(c=0;c<d;c++)if(!na(a[c],b[c]))return!1;return!0}}else{if(ja(a))return ja(b)?na(a.getTime(),
b.getTime()):!1;if(Za(a))return Za(b)?a.toString()===b.toString():!1;if(ab(a)||ab(b)||Ya(a)||Ya(b)||I(b)||ja(b)||Za(b))return!1;d=V();for(c in a)if("$"!==c.charAt(0)&&!C(a[c])){if(!na(a[c],b[c]))return!1;d[c]=!0}for(c in b)if(!(c in d)&&"$"!==c.charAt(0)&&x(b[c])&&!C(b[c]))return!1;return!0}return!1}function cb(a,b,d){return a.concat(va.call(b,d))}function db(a,b){var d=2<arguments.length?va.call(arguments,2):[];return!C(b)||b instanceof RegExp?b:d.length?function(){return arguments.length?b.apply(a,
cb(d,arguments,0)):b.apply(a,d)}:function(){return arguments.length?b.apply(a,arguments):b.call(a)}}function pe(a,b){var d=b;"string"===typeof a&&"$"===a.charAt(0)&&"$"===a.charAt(1)?d=void 0:Ya(b)?d="$WINDOW":b&&y.document===b?d="$DOCUMENT":ab(b)&&(d="$SCOPE");return d}function eb(a,b){if(!z(a))return ba(b)||(b=b?2:null),JSON.stringify(a,pe,b)}function Cc(a){return D(a)?JSON.parse(a):a}function Dc(a,b){a=a.replace(qe,"");var d=Date.parse("Jan 01, 1970 00:00:00 "+a)/6E4;return ia(d)?b:d}function Ub(a,
b,d){d=d?-1:1;var c=a.getTimezoneOffset();b=Dc(b,c);d*=b-c;a=new Date(a.getTime());a.setMinutes(a.getMinutes()+d);return a}function ya(a){a=F(a).clone();try{a.empty()}catch(b){}var d=F("<div>").append(a).html();try{return a[0].nodeType===La?Q(d):d.match(/^(<[^>]+>)/)[1].replace(/^<([\w-]+)/,function(a,b){return"<"+Q(b)})}catch(c){return Q(d)}}function Ec(a){try{return decodeURIComponent(a)}catch(b){}}function Fc(a){var b={};q((a||"").split("&"),function(a){var c,f,e;a&&(f=a=a.replace(/\+/g,"%20"),
c=a.indexOf("="),-1!==c&&(f=a.substring(0,c),e=a.substring(c+1)),f=Ec(f),x(f)&&(e=x(e)?Ec(e):!0,ua.call(b,f)?I(b[f])?b[f].push(e):b[f]=[b[f],e]:b[f]=e))});return b}function Vb(a){var b=[];q(a,function(a,c){I(a)?q(a,function(a){b.push(oa(c,!0)+(!0===a?"":"="+oa(a,!0)))}):b.push(oa(c,!0)+(!0===a?"":"="+oa(a,!0)))});return b.length?b.join("&"):""}function tb(a){return oa(a,!0).replace(/%26/gi,"&").replace(/%3D/gi,"=").replace(/%2B/gi,"+")}function oa(a,b){return encodeURIComponent(a).replace(/%40/gi,
"@").replace(/%3A/gi,":").replace(/%24/g,"$").replace(/%2C/gi,",").replace(/%3B/gi,";").replace(/%20/g,b?"%20":"+")}function re(a,b){var d,c,f=Oa.length;for(c=0;c<f;++c)if(d=Oa[c]+b,D(d=a.getAttribute(d)))return d;return null}function se(a,b){var d,c,f={};q(Oa,function(b){b+="app";!d&&a.hasAttribute&&a.hasAttribute(b)&&(d=a,c=a.getAttribute(b))});q(Oa,function(b){b+="app";var f;!d&&(f=a.querySelector("["+b.replace(":","\\:")+"]"))&&(d=f,c=f.getAttribute(b))});d&&(te?(f.strictDi=null!==re(d,"strict-di"),
b(d,c?[c]:[],f)):y.console.error("Angular: disabling automatic bootstrap. <script> protocol indicates an extension, document.location.href does not match."))}function Gc(a,b,d){E(d)||(d={});d=R({strictDi:!1},d);var c=function(){a=F(a);if(a.injector()){var c=a[0]===y.document?"document":ya(a);throw xa("btstrpd",c.replace(/</,"&lt;").replace(/>/,"&gt;"));}b=b||[];b.unshift(["$provide",function(b){b.value("$rootElement",a)}]);d.debugInfoEnabled&&b.push(["$compileProvider",function(a){a.debugInfoEnabled(!0)}]);
b.unshift("ng");c=fb(b,d.strictDi);c.invoke(["$rootScope","$rootElement","$compile","$injector",function(a,b,c,d){a.$apply(function(){b.data("$injector",d);c(b)(a)})}]);return c},f=/^NG_ENABLE_DEBUG_INFO!/,e=/^NG_DEFER_BOOTSTRAP!/;y&&f.test(y.name)&&(d.debugInfoEnabled=!0,y.name=y.name.replace(f,""));if(y&&!e.test(y.name))return c();y.name=y.name.replace(e,"");$.resumeBootstrap=function(a){q(a,function(a){b.push(a)});return c()};C($.resumeDeferredBootstrap)&&$.resumeDeferredBootstrap()}function ue(){y.name=
"NG_ENABLE_DEBUG_INFO!"+y.name;y.location.reload()}function ve(a){a=$.element(a).injector();if(!a)throw xa("test");return a.get("$$testability")}function Hc(a,b){b=b||"_";return a.replace(we,function(a,c){return(c?b:"")+a.toLowerCase()})}function xe(){var a;if(!Ic){var b=ub();(za=z(b)?y.jQuery:b?y[b]:void 0)&&za.fn.on?(F=za,R(za.fn,{scope:Pa.scope,isolateScope:Pa.isolateScope,controller:Pa.controller,injector:Pa.injector,inheritedData:Pa.inheritedData}),a=za.cleanData,za.cleanData=function(b){for(var c,
f=0,e;null!=(e=b[f]);f++)(c=za._data(e,"events"))&&c.$destroy&&za(e).triggerHandler("$destroy");a(b)}):F=W;$.element=F;Ic=!0}}function gb(a,b,d){if(!a)throw xa("areq",b||"?",d||"required");return a}function Qa(a,b,d){d&&I(a)&&(a=a[a.length-1]);gb(C(a),b,"not a function, got "+(a&&"object"===typeof a?a.constructor.name||"Object":typeof a));return a}function Ra(a,b){if("hasOwnProperty"===a)throw xa("badname",b);}function Jc(a,b,d){if(!b)return a;b=b.split(".");for(var c,f=a,e=b.length,g=0;g<e;g++)c=
b[g],a&&(a=(f=a)[c]);return!d&&C(a)?db(f,a):a}function vb(a){for(var b=a[0],d=a[a.length-1],c,f=1;b!==d&&(b=b.nextSibling);f++)if(c||a[f]!==b)c||(c=F(va.call(a,0,f))),c.push(b);return c||a}function V(){return Object.create(null)}function ye(a){function b(a,b,c){return a[b]||(a[b]=c())}var d=G("$injector"),c=G("ng");a=b(a,"angular",Object);a.$$minErr=a.$$minErr||G;return b(a,"module",function(){var a={};return function(e,g,h){if("hasOwnProperty"===e)throw c("badname","module");g&&a.hasOwnProperty(e)&&
(a[e]=null);return b(a,e,function(){function a(b,d,e,f){f||(f=c);return function(){f[e||"push"]([b,d,arguments]);return H}}function b(a,d){return function(b,f){f&&C(f)&&(f.$$moduleName=e);c.push([a,d,arguments]);return H}}if(!g)throw d("nomod",e);var c=[],f=[],r=[],s=a("$injector","invoke","push",f),H={_invokeQueue:c,_configBlocks:f,_runBlocks:r,requires:g,name:e,provider:b("$provide","provider"),factory:b("$provide","factory"),service:b("$provide","service"),value:a("$provide","value"),constant:a("$provide",
"constant","unshift"),decorator:b("$provide","decorator"),animation:b("$animateProvider","register"),filter:b("$filterProvider","register"),controller:b("$controllerProvider","register"),directive:b("$compileProvider","directive"),component:b("$compileProvider","component"),config:s,run:function(a){r.push(a);return this}};h&&s(h);return H})}})}function ka(a,b){if(I(a)){b=b||[];for(var d=0,c=a.length;d<c;d++)b[d]=a[d]}else if(E(a))for(d in b=b||{},a)if("$"!==d.charAt(0)||"$"!==d.charAt(1))b[d]=a[d];
return b||a}function ze(a){R(a,{bootstrap:Gc,copy:sa,extend:R,merge:le,equals:na,element:F,forEach:q,injector:fb,noop:w,bind:db,toJson:eb,fromJson:Cc,identity:$a,isUndefined:z,isDefined:x,isString:D,isFunction:C,isObject:E,isNumber:ba,isElement:Sb,isArray:I,version:Ae,isDate:ja,lowercase:Q,uppercase:wb,callbacks:{$$counter:0},getTestability:ve,$$minErr:G,$$csp:da,reloadWithDebugInfo:ue});Wb=ye(y);Wb("ng",["ngLocale"],["$provide",function(a){a.provider({$$sanitizeUri:Be});a.provider("$compile",Kc).directive({a:Ce,
input:Lc,textarea:Lc,form:De,script:Ee,select:Fe,option:Ge,ngBind:He,ngBindHtml:Ie,ngBindTemplate:Je,ngClass:Ke,ngClassEven:Le,ngClassOdd:Me,ngCloak:Ne,ngController:Oe,ngForm:Pe,ngHide:Qe,ngIf:Re,ngInclude:Se,ngInit:Te,ngNonBindable:Ue,ngPluralize:Ve,ngRepeat:We,ngShow:Xe,ngStyle:Ye,ngSwitch:Ze,ngSwitchWhen:$e,ngSwitchDefault:af,ngOptions:bf,ngTransclude:cf,ngModel:df,ngList:ef,ngChange:ff,pattern:Mc,ngPattern:Mc,required:Nc,ngRequired:Nc,minlength:Oc,ngMinlength:Oc,maxlength:Pc,ngMaxlength:Pc,ngValue:gf,
ngModelOptions:hf}).directive({ngInclude:jf}).directive(xb).directive(Qc);a.provider({$anchorScroll:kf,$animate:lf,$animateCss:mf,$$animateJs:nf,$$animateQueue:of,$$AnimateRunner:pf,$$animateAsyncRun:qf,$browser:rf,$cacheFactory:sf,$controller:tf,$document:uf,$exceptionHandler:vf,$filter:Rc,$$forceReflow:wf,$interpolate:xf,$interval:yf,$http:zf,$httpParamSerializer:Af,$httpParamSerializerJQLike:Bf,$httpBackend:Cf,$xhrFactory:Df,$jsonpCallbacks:Ef,$location:Ff,$log:Gf,$parse:Hf,$rootScope:If,$q:Jf,
$$q:Kf,$sce:Lf,$sceDelegate:Mf,$sniffer:Nf,$templateCache:Of,$templateRequest:Pf,$$testability:Qf,$timeout:Rf,$window:Sf,$$rAF:Tf,$$jqLite:Uf,$$HashMap:Vf,$$cookieReader:Wf})}])}function hb(a){return a.replace(Xf,function(a,d,c,f){return f?c.toUpperCase():c}).replace(Yf,"Moz$1")}function Sc(a){a=a.nodeType;return 1===a||!a||9===a}function Tc(a,b){var d,c,f=b.createDocumentFragment(),e=[];if(Xb.test(a)){d=f.appendChild(b.createElement("div"));c=(Zf.exec(a)||["",""])[1].toLowerCase();c=pa[c]||pa._default;
d.innerHTML=c[1]+a.replace($f,"<$1></$2>")+c[2];for(c=c[0];c--;)d=d.lastChild;e=cb(e,d.childNodes);d=f.firstChild;d.textContent=""}else e.push(b.createTextNode(a));f.textContent="";f.innerHTML="";q(e,function(a){f.appendChild(a)});return f}function Uc(a,b){var d=a.parentNode;d&&d.replaceChild(b,a);b.appendChild(a)}function W(a){if(a instanceof W)return a;var b;D(a)&&(a=Y(a),b=!0);if(!(this instanceof W)){if(b&&"<"!==a.charAt(0))throw Yb("nosel");return new W(a)}if(b){b=y.document;var d;a=(d=ag.exec(a))?
[b.createElement(d[1])]:(d=Tc(a,b))?d.childNodes:[]}Vc(this,a)}function Zb(a){return a.cloneNode(!0)}function yb(a,b){b||ib(a);if(a.querySelectorAll)for(var d=a.querySelectorAll("*"),c=0,f=d.length;c<f;c++)ib(d[c])}function Wc(a,b,d,c){if(x(c))throw Yb("offargs");var f=(c=zb(a))&&c.events,e=c&&c.handle;if(e)if(b){var g=function(b){var c=f[b];x(d)&&bb(c||[],d);x(d)&&c&&0<c.length||(a.removeEventListener(b,e,!1),delete f[b])};q(b.split(" "),function(a){g(a);Ab[a]&&g(Ab[a])})}else for(b in f)"$destroy"!==
b&&a.removeEventListener(b,e,!1),delete f[b]}function ib(a,b){var d=a.ng339,c=d&&jb[d];c&&(b?delete c.data[b]:(c.handle&&(c.events.$destroy&&c.handle({},"$destroy"),Wc(a)),delete jb[d],a.ng339=void 0))}function zb(a,b){var d=a.ng339,d=d&&jb[d];b&&!d&&(a.ng339=d=++bg,d=jb[d]={events:{},data:{},handle:void 0});return d}function $b(a,b,d){if(Sc(a)){var c=x(d),f=!c&&b&&!E(b),e=!b;a=(a=zb(a,!f))&&a.data;if(c)a[b]=d;else{if(e)return a;if(f)return a&&a[b];R(a,b)}}}function Bb(a,b){return a.getAttribute?
-1<(" "+(a.getAttribute("class")||"")+" ").replace(/[\n\t]/g," ").indexOf(" "+b+" "):!1}function Cb(a,b){b&&a.setAttribute&&q(b.split(" "),function(b){a.setAttribute("class",Y((" "+(a.getAttribute("class")||"")+" ").replace(/[\n\t]/g," ").replace(" "+Y(b)+" "," ")))})}function Db(a,b){if(b&&a.setAttribute){var d=(" "+(a.getAttribute("class")||"")+" ").replace(/[\n\t]/g," ");q(b.split(" "),function(a){a=Y(a);-1===d.indexOf(" "+a+" ")&&(d+=a+" ")});a.setAttribute("class",Y(d))}}function Vc(a,b){if(b)if(b.nodeType)a[a.length++]=
b;else{var d=b.length;if("number"===typeof d&&b.window!==b){if(d)for(var c=0;c<d;c++)a[a.length++]=b[c]}else a[a.length++]=b}}function Xc(a,b){return Eb(a,"$"+(b||"ngController")+"Controller")}function Eb(a,b,d){9===a.nodeType&&(a=a.documentElement);for(b=I(b)?b:[b];a;){for(var c=0,f=b.length;c<f;c++)if(x(d=F.data(a,b[c])))return d;a=a.parentNode||11===a.nodeType&&a.host}}function Yc(a){for(yb(a,!0);a.firstChild;)a.removeChild(a.firstChild)}function Fb(a,b){b||yb(a);var d=a.parentNode;d&&d.removeChild(a)}
function cg(a,b){b=b||y;if("complete"===b.document.readyState)b.setTimeout(a);else F(b).on("load",a)}function Zc(a,b){var d=Gb[b.toLowerCase()];return d&&$c[wa(a)]&&d}function dg(a,b){var d=function(c,d){c.isDefaultPrevented=function(){return c.defaultPrevented};var e=b[d||c.type],g=e?e.length:0;if(g){if(z(c.immediatePropagationStopped)){var h=c.stopImmediatePropagation;c.stopImmediatePropagation=function(){c.immediatePropagationStopped=!0;c.stopPropagation&&c.stopPropagation();h&&h.call(c)}}c.isImmediatePropagationStopped=
function(){return!0===c.immediatePropagationStopped};var k=e.specialHandlerWrapper||eg;1<g&&(e=ka(e));for(var l=0;l<g;l++)c.isImmediatePropagationStopped()||k(a,c,e[l])}};d.elem=a;return d}function eg(a,b,d){d.call(a,b)}function fg(a,b,d){var c=b.relatedTarget;c&&(c===a||gg.call(a,c))||d.call(a,b)}function Uf(){this.$get=function(){return R(W,{hasClass:function(a,b){a.attr&&(a=a[0]);return Bb(a,b)},addClass:function(a,b){a.attr&&(a=a[0]);return Db(a,b)},removeClass:function(a,b){a.attr&&(a=a[0]);
return Cb(a,b)}})}}function Aa(a,b){var d=a&&a.$$hashKey;if(d)return"function"===typeof d&&(d=a.$$hashKey()),d;d=typeof a;return d="function"===d||"object"===d&&null!==a?a.$$hashKey=d+":"+(b||ke)():d+":"+a}function Sa(a,b){if(b){var d=0;this.nextUid=function(){return++d}}q(a,this.put,this)}function ad(a){a=(Function.prototype.toString.call(a)+" ").replace(hg,"");return a.match(ig)||a.match(jg)}function kg(a){return(a=ad(a))?"function("+(a[1]||"").replace(/[\s\r\n]+/," ")+")":"fn"}function fb(a,b){function d(a){return function(b,
c){if(E(b))q(b,zc(a));else return a(b,c)}}function c(a,b){Ra(a,"service");if(C(b)||I(b))b=r.instantiate(b);if(!b.$get)throw Ba("pget",a);return n[a+"Provider"]=b}function f(a,b){return function(){var c=u.invoke(b,this);if(z(c))throw Ba("undef",a);return c}}function e(a,b,d){return c(a,{$get:!1!==d?f(a,b):b})}function g(a){gb(z(a)||I(a),"modulesToLoad","not an array");var b=[],c;q(a,function(a){function d(a){var b,c;b=0;for(c=a.length;b<c;b++){var e=a[b],f=r.get(e[0]);f[e[1]].apply(f,e[2])}}if(!m.get(a)){m.put(a,
!0);try{D(a)?(c=Wb(a),b=b.concat(g(c.requires)).concat(c._runBlocks),d(c._invokeQueue),d(c._configBlocks)):C(a)?b.push(r.invoke(a)):I(a)?b.push(r.invoke(a)):Qa(a,"module")}catch(e){throw I(a)&&(a=a[a.length-1]),e.message&&e.stack&&-1===e.stack.indexOf(e.message)&&(e=e.message+"\n"+e.stack),Ba("modulerr",a,e.stack||e.message||e);}}});return b}function h(a,c){function d(b,e){if(a.hasOwnProperty(b)){if(a[b]===k)throw Ba("cdep",b+" <- "+l.join(" <- "));return a[b]}try{return l.unshift(b),a[b]=k,a[b]=
c(b,e),a[b]}catch(f){throw a[b]===k&&delete a[b],f;}finally{l.shift()}}function e(a,c,f){var g=[];a=fb.$$annotate(a,b,f);for(var h=0,k=a.length;h<k;h++){var l=a[h];if("string"!==typeof l)throw Ba("itkn",l);g.push(c&&c.hasOwnProperty(l)?c[l]:d(l,f))}return g}return{invoke:function(a,b,c,d){"string"===typeof c&&(d=c,c=null);c=e(a,c,d);I(a)&&(a=a[a.length-1]);d=11>=Ia?!1:"function"===typeof a&&/^(?:class\b|constructor\()/.test(Function.prototype.toString.call(a)+" ");return d?(c.unshift(null),new (Function.prototype.bind.apply(a,
c))):a.apply(b,c)},instantiate:function(a,b,c){var d=I(a)?a[a.length-1]:a;a=e(a,b,c);a.unshift(null);return new (Function.prototype.bind.apply(d,a))},get:d,annotate:fb.$$annotate,has:function(b){return n.hasOwnProperty(b+"Provider")||a.hasOwnProperty(b)}}}b=!0===b;var k={},l=[],m=new Sa([],!0),n={$provide:{provider:d(c),factory:d(e),service:d(function(a,b){return e(a,["$injector",function(a){return a.instantiate(b)}])}),value:d(function(a,b){return e(a,ha(b),!1)}),constant:d(function(a,b){Ra(a,"constant");
n[a]=b;s[a]=b}),decorator:function(a,b){var c=r.get(a+"Provider"),d=c.$get;c.$get=function(){var a=u.invoke(d,c);return u.invoke(b,null,{$delegate:a})}}}},r=n.$injector=h(n,function(a,b){$.isString(b)&&l.push(b);throw Ba("unpr",l.join(" <- "));}),s={},H=h(s,function(a,b){var c=r.get(a+"Provider",b);return u.invoke(c.$get,c,void 0,a)}),u=H;n.$injectorProvider={$get:ha(H)};var p=g(a),u=H.get("$injector");u.strictDi=b;q(p,function(a){a&&u.invoke(a)});return u}function kf(){var a=!0;this.disableAutoScrolling=
function(){a=!1};this.$get=["$window","$location","$rootScope",function(b,d,c){function f(a){var b=null;Array.prototype.some.call(a,function(a){if("a"===wa(a))return b=a,!0});return b}function e(a){if(a){a.scrollIntoView();var c;c=g.yOffset;C(c)?c=c():Sb(c)?(c=c[0],c="fixed"!==b.getComputedStyle(c).position?0:c.getBoundingClientRect().bottom):ba(c)||(c=0);c&&(a=a.getBoundingClientRect().top,b.scrollBy(0,a-c))}else b.scrollTo(0,0)}function g(a){a=D(a)?a:ba(a)?a.toString():d.hash();var b;a?(b=h.getElementById(a))?
e(b):(b=f(h.getElementsByName(a)))?e(b):"top"===a&&e(null):e(null)}var h=b.document;a&&c.$watch(function(){return d.hash()},function(a,b){a===b&&""===a||cg(function(){c.$evalAsync(g)})});return g}]}function kb(a,b){if(!a&&!b)return"";if(!a)return b;if(!b)return a;I(a)&&(a=a.join(" "));I(b)&&(b=b.join(" "));return a+" "+b}function lg(a){D(a)&&(a=a.split(" "));var b=V();q(a,function(a){a.length&&(b[a]=!0)});return b}function Ca(a){return E(a)?a:{}}function mg(a,b,d,c){function f(a){try{a.apply(null,
va.call(arguments,1))}finally{if(H--,0===H)for(;u.length;)try{u.pop()()}catch(b){d.error(b)}}}function e(){N=null;g();h()}function g(){p=L();p=z(p)?null:p;na(p,J)&&(p=J);J=p}function h(){if(A!==k.url()||K!==p)A=k.url(),K=p,q(O,function(a){a(k.url(),p)})}var k=this,l=a.location,m=a.history,n=a.setTimeout,r=a.clearTimeout,s={};k.isMock=!1;var H=0,u=[];k.$$completeOutstandingRequest=f;k.$$incOutstandingRequestCount=function(){H++};k.notifyWhenNoOutstandingRequests=function(a){0===H?a():u.push(a)};var p,
K,A=l.href,v=b.find("base"),N=null,L=c.history?function(){try{return m.state}catch(a){}}:w;g();K=p;k.url=function(b,d,e){z(e)&&(e=null);l!==a.location&&(l=a.location);m!==a.history&&(m=a.history);if(b){var f=K===e;if(A===b&&(!c.history||f))return k;var h=A&&Ga(A)===Ga(b);A=b;K=e;!c.history||h&&f?(h||(N=b),d?l.replace(b):h?(d=l,e=b.indexOf("#"),e=-1===e?"":b.substr(e),d.hash=e):l.href=b,l.href!==b&&(N=b)):(m[d?"replaceState":"pushState"](e,"",b),g(),K=p);N&&(N=b);return k}return N||l.href.replace(/%27/g,
"'")};k.state=function(){return p};var O=[],M=!1,J=null;k.onUrlChange=function(b){if(!M){if(c.history)F(a).on("popstate",e);F(a).on("hashchange",e);M=!0}O.push(b);return b};k.$$applicationDestroyed=function(){F(a).off("hashchange popstate",e)};k.$$checkUrlChange=h;k.baseHref=function(){var a=v.attr("href");return a?a.replace(/^(https?:)?\/\/[^/]*/,""):""};k.defer=function(a,b){var c;H++;c=n(function(){delete s[c];f(a)},b||0);s[c]=!0;return c};k.defer.cancel=function(a){return s[a]?(delete s[a],r(a),
f(w),!0):!1}}function rf(){this.$get=["$window","$log","$sniffer","$document",function(a,b,d,c){return new mg(a,c,b,d)}]}function sf(){this.$get=function(){function a(a,c){function f(a){a!==n&&(r?r===a&&(r=a.n):r=a,e(a.n,a.p),e(a,n),n=a,n.n=null)}function e(a,b){a!==b&&(a&&(a.p=b),b&&(b.n=a))}if(a in b)throw G("$cacheFactory")("iid",a);var g=0,h=R({},c,{id:a}),k=V(),l=c&&c.capacity||Number.MAX_VALUE,m=V(),n=null,r=null;return b[a]={put:function(a,b){if(!z(b)){if(l<Number.MAX_VALUE){var c=m[a]||(m[a]=
{key:a});f(c)}a in k||g++;k[a]=b;g>l&&this.remove(r.key);return b}},get:function(a){if(l<Number.MAX_VALUE){var b=m[a];if(!b)return;f(b)}return k[a]},remove:function(a){if(l<Number.MAX_VALUE){var b=m[a];if(!b)return;b===n&&(n=b.p);b===r&&(r=b.n);e(b.n,b.p);delete m[a]}a in k&&(delete k[a],g--)},removeAll:function(){k=V();g=0;m=V();n=r=null},destroy:function(){m=h=k=null;delete b[a]},info:function(){return R({},h,{size:g})}}}var b={};a.info=function(){var a={};q(b,function(b,f){a[f]=b.info()});return a};
a.get=function(a){return b[a]};return a}}function Of(){this.$get=["$cacheFactory",function(a){return a("templates")}]}function Kc(a,b){function d(a,b,c){var d=/^\s*([@&<]|=(\*?))(\??)\s*([\w$]*)\s*$/,e=V();q(a,function(a,f){if(a in n)e[f]=n[a];else{var g=a.match(d);if(!g)throw fa("iscp",b,f,a,c?"controller bindings definition":"isolate scope definition");e[f]={mode:g[1][0],collection:"*"===g[2],optional:"?"===g[3],attrName:g[4]||f};g[4]&&(n[a]=e[f])}});return e}function c(a){var b=a.charAt(0);if(!b||
b!==Q(b))throw fa("baddir",a);if(a!==a.trim())throw fa("baddir",a);}function f(a){var b=a.require||a.controller&&a.name;!I(b)&&E(b)&&q(b,function(a,c){var d=a.match(l);a.substring(d[0].length)||(b[c]=d[0]+c)});return b}var e={},g=/^\s*directive:\s*([\w-]+)\s+(.*)$/,h=/(([\w-]+)(?::([^;]+))?;?)/,k=oe("ngSrc,ngSrcset,src,srcset"),l=/^(?:(\^\^?)?(\?)?(\^\^?)?)?/,m=/^(on[a-z]+|formaction)$/,n=V();this.directive=function A(b,d){gb(b,"name");Ra(b,"directive");D(b)?(c(b),gb(d,"directiveFactory"),e.hasOwnProperty(b)||
(e[b]=[],a.factory(b+"Directive",["$injector","$exceptionHandler",function(a,c){var d=[];q(e[b],function(e,g){try{var h=a.invoke(e);C(h)?h={compile:ha(h)}:!h.compile&&h.link&&(h.compile=ha(h.link));h.priority=h.priority||0;h.index=g;h.name=h.name||b;h.require=f(h);var k=h,l=h.restrict;if(l&&(!D(l)||!/[EACM]/.test(l)))throw fa("badrestrict",l,b);k.restrict=l||"EA";h.$$moduleName=e.$$moduleName;d.push(h)}catch(m){c(m)}});return d}])),e[b].push(d)):q(b,zc(A));return this};this.component=function(a,b){function c(a){function e(b){return C(b)||
I(b)?function(c,d){return a.invoke(b,this,{$element:c,$attrs:d})}:b}var f=b.template||b.templateUrl?b.template:"",g={controller:d,controllerAs:ng(b.controller)||b.controllerAs||"$ctrl",template:e(f),templateUrl:e(b.templateUrl),transclude:b.transclude,scope:{},bindToController:b.bindings||{},restrict:"E",require:b.require};q(b,function(a,b){"$"===b.charAt(0)&&(g[b]=a)});return g}var d=b.controller||function(){};q(b,function(a,b){"$"===b.charAt(0)&&(c[b]=a,C(d)&&(d[b]=a))});c.$inject=["$injector"];
return this.directive(a,c)};this.aHrefSanitizationWhitelist=function(a){return x(a)?(b.aHrefSanitizationWhitelist(a),this):b.aHrefSanitizationWhitelist()};this.imgSrcSanitizationWhitelist=function(a){return x(a)?(b.imgSrcSanitizationWhitelist(a),this):b.imgSrcSanitizationWhitelist()};var r=!0;this.debugInfoEnabled=function(a){return x(a)?(r=a,this):r};var s=!0;this.preAssignBindingsEnabled=function(a){return x(a)?(s=a,this):s};var H=10;this.onChangesTtl=function(a){return arguments.length?(H=a,this):
H};var u=!0;this.commentDirectivesEnabled=function(a){return arguments.length?(u=a,this):u};var p=!0;this.cssClassDirectivesEnabled=function(a){return arguments.length?(p=a,this):p};this.$get=["$injector","$interpolate","$exceptionHandler","$templateRequest","$parse","$controller","$rootScope","$sce","$animate","$$sanitizeUri",function(a,b,c,f,n,M,J,B,T,S){function P(){try{if(!--xa)throw da=void 0,fa("infchng",H);J.$apply(function(){for(var a=[],b=0,c=da.length;b<c;++b)try{da[b]()}catch(d){a.push(d)}da=
void 0;if(a.length)throw a;})}finally{xa++}}function t(a,b){if(b){var c=Object.keys(b),d,e,f;d=0;for(e=c.length;d<e;d++)f=c[d],this[f]=b[f]}else this.$attr={};this.$$element=a}function qa(a,b,c){ta.innerHTML="<span "+b+">";b=ta.firstChild.attributes;var d=b[0];b.removeNamedItem(d.name);d.value=c;a.attributes.setNamedItem(d)}function Ja(a,b){try{a.addClass(b)}catch(c){}}function ca(a,b,c,d,e){a instanceof F||(a=F(a));for(var f=/\S+/,g=0,h=a.length;g<h;g++){var k=a[g];k.nodeType===La&&k.nodeValue.match(f)&&
Uc(k,a[g]=y.document.createElement("span"))}var l=Ma(a,b,a,c,d,e);ca.$$addScopeClass(a);var m=null;return function(b,c,d){gb(b,"scope");e&&e.needsNewScope&&(b=b.$parent.$new());d=d||{};var f=d.parentBoundTranscludeFn,g=d.transcludeControllers;d=d.futureParentElement;f&&f.$$boundTransclude&&(f=f.$$boundTransclude);m||(m=(d=d&&d[0])?"foreignobject"!==wa(d)&&ma.call(d).match(/SVG/)?"svg":"html":"html");d="html"!==m?F(ha(m,F("<div>").append(a).html())):c?Pa.clone.call(a):a;if(g)for(var h in g)d.data("$"+
h+"Controller",g[h].instance);ca.$$addScopeInfo(d,b);c&&c(d,b);l&&l(b,d,d,f);return d}}function Ma(a,b,c,d,e,f){function g(a,c,d,e){var f,k,l,m,n,s,A;if(p)for(A=Array(c.length),m=0;m<h.length;m+=3)f=h[m],A[f]=c[f];else A=c;m=0;for(n=h.length;m<n;)k=A[h[m++]],c=h[m++],f=h[m++],c?(c.scope?(l=a.$new(),ca.$$addScopeInfo(F(k),l)):l=a,s=c.transcludeOnThisElement?G(a,c.transclude,e):!c.templateOnThisElement&&e?e:!e&&b?G(a,b):null,c(f,l,k,d,s)):f&&f(a,k.childNodes,void 0,e)}for(var h=[],k,l,m,n,p,s=0;s<a.length;s++){k=
new t;l=cc(a[s],[],k,0===s?d:void 0,e);(f=l.length?W(l,a[s],k,b,c,null,[],[],f):null)&&f.scope&&ca.$$addScopeClass(k.$$element);k=f&&f.terminal||!(m=a[s].childNodes)||!m.length?null:Ma(m,f?(f.transcludeOnThisElement||!f.templateOnThisElement)&&f.transclude:b);if(f||k)h.push(s,f,k),n=!0,p=p||f;f=null}return n?g:null}function G(a,b,c){function d(e,f,g,h,k){e||(e=a.$new(!1,k),e.$$transcluded=!0);return b(e,f,{parentBoundTranscludeFn:c,transcludeControllers:g,futureParentElement:h})}var e=d.$$slots=V(),
f;for(f in b.$$slots)e[f]=b.$$slots[f]?G(a,b.$$slots[f],c):null;return d}function cc(a,b,c,d,e){var f=c.$attr,g;switch(a.nodeType){case 1:g=wa(a);U(b,Da(g),"E",d,e);for(var k,l,m,n,p=a.attributes,s=0,A=p&&p.length;s<A;s++){var r=!1,u=!1;k=p[s];l=k.name;m=Y(k.value);k=Da(l);(n=Ga.test(k))&&(l=l.replace(bd,"").substr(8).replace(/_(.)/g,function(a,b){return b.toUpperCase()}));(k=k.match(Ha))&&Z(k[1])&&(r=l,u=l.substr(0,l.length-5)+"end",l=l.substr(0,l.length-6));k=Da(l.toLowerCase());f[k]=l;if(n||!c.hasOwnProperty(k))c[k]=
m,Zc(a,k)&&(c[k]=!0);pa(a,b,m,k,n);U(b,k,"A",d,e,r,u)}"input"===g&&"hidden"===a.getAttribute("type")&&a.setAttribute("autocomplete","off");if(!Fa)break;f=a.className;E(f)&&(f=f.animVal);if(D(f)&&""!==f)for(;a=h.exec(f);)k=Da(a[2]),U(b,k,"C",d,e)&&(c[k]=Y(a[3])),f=f.substr(a.index+a[0].length);break;case La:if(11===Ia)for(;a.parentNode&&a.nextSibling&&a.nextSibling.nodeType===La;)a.nodeValue+=a.nextSibling.nodeValue,a.parentNode.removeChild(a.nextSibling);ka(b,a.nodeValue);break;case 8:if(!Ea)break;
Ta(a,b,c,d,e)}b.sort(ja);return b}function Ta(a,b,c,d,e){try{var f=g.exec(a.nodeValue);if(f){var h=Da(f[1]);U(b,h,"M",d,e)&&(c[h]=Y(f[2]))}}catch(k){}}function cd(a,b,c){var d=[],e=0;if(b&&a.hasAttribute&&a.hasAttribute(b)){do{if(!a)throw fa("uterdir",b,c);1===a.nodeType&&(a.hasAttribute(b)&&e++,a.hasAttribute(c)&&e--);d.push(a);a=a.nextSibling}while(0<e)}else d.push(a);return F(d)}function dd(a,b,c){return function(d,e,f,g,h){e=cd(e[0],b,c);return a(d,e,f,g,h)}}function dc(a,b,c,d,e,f){var g;return a?
ca(b,c,d,e,f):function(){g||(g=ca(b,c,d,e,f),b=c=f=null);return g.apply(this,arguments)}}function W(a,b,d,e,f,g,h,k,l){function m(a,b,c,d){if(a){c&&(a=dd(a,c,d));a.require=v.require;a.directiveName=S;if(u===v||v.$$isolateScope)a=ra(a,{isolateScope:!0});h.push(a)}if(b){c&&(b=dd(b,c,d));b.require=v.require;b.directiveName=S;if(u===v||v.$$isolateScope)b=ra(b,{isolateScope:!0});k.push(b)}}function n(a,e,f,g,l){function m(a,b,c,d){var e;ab(a)||(d=c,c=b,b=a,a=void 0);H&&(e=J);c||(c=H?P.parent():P);if(d){var f=
l.$$slots[d];if(f)return f(a,b,e,c,qa);if(z(f))throw fa("noslot",d,ya(P));}else return l(a,b,e,c,qa)}var p,v,B,M,T,J,S,P;b===f?(g=d,P=d.$$element):(P=F(f),g=new t(P,d));T=e;u?M=e.$new(!0):A&&(T=e.$parent);l&&(S=m,S.$$boundTransclude=l,S.isSlotFilled=function(a){return!!l.$$slots[a]});r&&(J=ba(P,g,S,r,M,e,u));u&&(ca.$$addScopeInfo(P,M,!0,!(O&&(O===u||O===u.$$originalDirective))),ca.$$addScopeClass(P,!0),M.$$isolateBindings=u.$$isolateBindings,v=la(e,g,M,M.$$isolateBindings,u),v.removeWatches&&M.$on("$destroy",
v.removeWatches));for(p in J){v=r[p];B=J[p];var L=v.$$bindings.bindToController;if(s){B.bindingInfo=L?la(T,g,B.instance,L,v):{};var ac=B();ac!==B.instance&&(B.instance=ac,P.data("$"+v.name+"Controller",ac),B.bindingInfo.removeWatches&&B.bindingInfo.removeWatches(),B.bindingInfo=la(T,g,B.instance,L,v))}else B.instance=B(),P.data("$"+v.name+"Controller",B.instance),B.bindingInfo=la(T,g,B.instance,L,v)}q(r,function(a,b){var c=a.require;a.bindToController&&!I(c)&&E(c)&&R(J[b].instance,X(b,c,P,J))});q(J,
function(a){var b=a.instance;if(C(b.$onChanges))try{b.$onChanges(a.bindingInfo.initialChanges)}catch(d){c(d)}if(C(b.$onInit))try{b.$onInit()}catch(e){c(e)}C(b.$doCheck)&&(T.$watch(function(){b.$doCheck()}),b.$doCheck());C(b.$onDestroy)&&T.$on("$destroy",function(){b.$onDestroy()})});p=0;for(v=h.length;p<v;p++)B=h[p],sa(B,B.isolateScope?M:e,P,g,B.require&&X(B.directiveName,B.require,P,J),S);var qa=e;u&&(u.template||null===u.templateUrl)&&(qa=M);a&&a(qa,f.childNodes,void 0,l);for(p=k.length-1;0<=p;p--)B=
k[p],sa(B,B.isolateScope?M:e,P,g,B.require&&X(B.directiveName,B.require,P,J),S);q(J,function(a){a=a.instance;C(a.$postLink)&&a.$postLink()})}l=l||{};for(var p=-Number.MAX_VALUE,A=l.newScopeDirective,r=l.controllerDirectives,u=l.newIsolateScopeDirective,O=l.templateDirective,M=l.nonTlbTranscludeDirective,T=!1,J=!1,H=l.hasElementTranscludeDirective,B=d.$$element=F(b),v,S,P,L=e,qa,x=!1,Ja=!1,w,y=0,D=a.length;y<D;y++){v=a[y];var Ta=v.$$start,Ma=v.$$end;Ta&&(B=cd(b,Ta,Ma));P=void 0;if(p>v.priority)break;
if(w=v.scope)v.templateUrl||(E(w)?($("new/isolated scope",u||A,v,B),u=v):$("new/isolated scope",u,v,B)),A=A||v;S=v.name;if(!x&&(v.replace&&(v.templateUrl||v.template)||v.transclude&&!v.$$tlb)){for(w=y+1;x=a[w++];)if(x.transclude&&!x.$$tlb||x.replace&&(x.templateUrl||x.template)){Ja=!0;break}x=!0}!v.templateUrl&&v.controller&&(r=r||V(),$("'"+S+"' controller",r[S],v,B),r[S]=v);if(w=v.transclude)if(T=!0,v.$$tlb||($("transclusion",M,v,B),M=v),"element"===w)H=!0,p=v.priority,P=B,B=d.$$element=F(ca.$$createComment(S,
d[S])),b=B[0],ga(f,va.call(P,0),b),P[0].$$parentNode=P[0].parentNode,L=dc(Ja,P,e,p,g&&g.name,{nonTlbTranscludeDirective:M});else{var G=V();P=F(Zb(b)).contents();if(E(w)){P=[];var Q=V(),bc=V();q(w,function(a,b){var c="?"===a.charAt(0);a=c?a.substring(1):a;Q[a]=b;G[b]=null;bc[b]=c});q(B.contents(),function(a){var b=Q[Da(wa(a))];b?(bc[b]=!0,G[b]=G[b]||[],G[b].push(a)):P.push(a)});q(bc,function(a,b){if(!a)throw fa("reqslot",b);});for(var U in G)G[U]&&(G[U]=dc(Ja,G[U],e))}B.empty();L=dc(Ja,P,e,void 0,
void 0,{needsNewScope:v.$$isolateScope||v.$$newScope});L.$$slots=G}if(v.template)if(J=!0,$("template",O,v,B),O=v,w=C(v.template)?v.template(B,d):v.template,w=Ca(w),v.replace){g=v;P=Xb.test(w)?ed(ha(v.templateNamespace,Y(w))):[];b=P[0];if(1!==P.length||1!==b.nodeType)throw fa("tplrt",S,"");ga(f,B,b);D={$attr:{}};w=cc(b,[],D);var og=a.splice(y+1,a.length-(y+1));(u||A)&&aa(w,u,A);a=a.concat(w).concat(og);ea(d,D);D=a.length}else B.html(w);if(v.templateUrl)J=!0,$("template",O,v,B),O=v,v.replace&&(g=v),
n=ia(a.splice(y,a.length-y),B,d,f,T&&L,h,k,{controllerDirectives:r,newScopeDirective:A!==v&&A,newIsolateScopeDirective:u,templateDirective:O,nonTlbTranscludeDirective:M}),D=a.length;else if(v.compile)try{qa=v.compile(B,d,L);var Z=v.$$originalDirective||v;C(qa)?m(null,db(Z,qa),Ta,Ma):qa&&m(db(Z,qa.pre),db(Z,qa.post),Ta,Ma)}catch(da){c(da,ya(B))}v.terminal&&(n.terminal=!0,p=Math.max(p,v.priority))}n.scope=A&&!0===A.scope;n.transcludeOnThisElement=T;n.templateOnThisElement=J;n.transclude=L;l.hasElementTranscludeDirective=
H;return n}function X(a,b,c,d){var e;if(D(b)){var f=b.match(l);b=b.substring(f[0].length);var g=f[1]||f[3],f="?"===f[2];"^^"===g?c=c.parent():e=(e=d&&d[b])&&e.instance;if(!e){var h="$"+b+"Controller";e=g?c.inheritedData(h):c.data(h)}if(!e&&!f)throw fa("ctreq",b,a);}else if(I(b))for(e=[],g=0,f=b.length;g<f;g++)e[g]=X(a,b[g],c,d);else E(b)&&(e={},q(b,function(b,f){e[f]=X(a,b,c,d)}));return e||null}function ba(a,b,c,d,e,f,g){var h=V(),k;for(k in d){var l=d[k],m={$scope:l===g||l.$$isolateScope?e:f,$element:a,
$attrs:b,$transclude:c},n=l.controller;"@"===n&&(n=b[l.name]);m=M(n,m,!0,l.controllerAs);h[l.name]=m;a.data("$"+l.name+"Controller",m.instance)}return h}function aa(a,b,c){for(var d=0,e=a.length;d<e;d++)a[d]=Tb(a[d],{$$isolateScope:b,$$newScope:c})}function U(b,c,f,g,h,k,l){if(c===h)return null;var m=null;if(e.hasOwnProperty(c)){h=a.get(c+"Directive");for(var n=0,p=h.length;n<p;n++)if(c=h[n],(z(g)||g>c.priority)&&-1!==c.restrict.indexOf(f)){k&&(c=Tb(c,{$$start:k,$$end:l}));if(!c.$$bindings){var s=
m=c,r=c.name,v={isolateScope:null,bindToController:null};E(s.scope)&&(!0===s.bindToController?(v.bindToController=d(s.scope,r,!0),v.isolateScope={}):v.isolateScope=d(s.scope,r,!1));E(s.bindToController)&&(v.bindToController=d(s.bindToController,r,!0));if(v.bindToController&&!s.controller)throw fa("noctrl",r);m=m.$$bindings=v;E(m.isolateScope)&&(c.$$isolateBindings=m.isolateScope)}b.push(c);m=c}}return m}function Z(b){if(e.hasOwnProperty(b))for(var c=a.get(b+"Directive"),d=0,f=c.length;d<f;d++)if(b=
c[d],b.multiElement)return!0;return!1}function ea(a,b){var c=b.$attr,d=a.$attr;q(a,function(d,e){"$"!==e.charAt(0)&&(b[e]&&b[e]!==d&&(d+=("style"===e?";":" ")+b[e]),a.$set(e,d,!0,c[e]))});q(b,function(b,e){a.hasOwnProperty(e)||"$"===e.charAt(0)||(a[e]=b,"class"!==e&&"style"!==e&&(d[e]=c[e]))})}function ia(a,b,c,d,e,g,h,k){var l=[],m,n,p=b[0],s=a.shift(),A=Tb(s,{templateUrl:null,transclude:null,replace:null,$$originalDirective:s}),r=C(s.templateUrl)?s.templateUrl(b,c):s.templateUrl,v=s.templateNamespace;
b.empty();f(r).then(function(f){var u,B;f=Ca(f);if(s.replace){f=Xb.test(f)?ed(ha(v,Y(f))):[];u=f[0];if(1!==f.length||1!==u.nodeType)throw fa("tplrt",s.name,r);f={$attr:{}};ga(d,b,u);var O=cc(u,[],f);E(s.scope)&&aa(O,!0);a=O.concat(a);ea(c,f)}else u=p,b.html(f);a.unshift(A);m=W(a,u,c,e,b,s,g,h,k);q(d,function(a,c){a===u&&(d[c]=b[0])});for(n=Ma(b[0].childNodes,e);l.length;){f=l.shift();B=l.shift();var M=l.shift(),T=l.shift(),O=b[0];if(!f.$$destroyed){if(B!==p){var J=B.className;k.hasElementTranscludeDirective&&
s.replace||(O=Zb(u));ga(M,F(B),O);Ja(F(O),J)}B=m.transcludeOnThisElement?G(f,m.transclude,T):T;m(n,f,O,d,B)}}l=null});return function(a,b,c,d,e){a=e;b.$$destroyed||(l?l.push(b,c,d,a):(m.transcludeOnThisElement&&(a=G(b,m.transclude,e)),m(n,b,c,d,a)))}}function ja(a,b){var c=b.priority-a.priority;return 0!==c?c:a.name!==b.name?a.name<b.name?-1:1:a.index-b.index}function $(a,b,c,d){function e(a){return a?" (module: "+a+")":""}if(b)throw fa("multidir",b.name,e(b.$$moduleName),c.name,e(c.$$moduleName),
a,ya(d));}function ka(a,c){var d=b(c,!0);d&&a.push({priority:0,compile:function(a){a=a.parent();var b=!!a.length;b&&ca.$$addBindingClass(a);return function(a,c){var e=c.parent();b||ca.$$addBindingClass(e);ca.$$addBindingInfo(e,d.expressions);a.$watch(d,function(a){c[0].nodeValue=a})}}})}function ha(a,b){a=Q(a||"html");switch(a){case "svg":case "math":var c=y.document.createElement("div");c.innerHTML="<"+a+">"+b+"</"+a+">";return c.childNodes[0].childNodes;default:return b}}function oa(a,b){if("srcdoc"===
b)return B.HTML;var c=wa(a);if("src"===b||"ngSrc"===b){if(-1===["img","video","audio","source","track"].indexOf(c))return B.RESOURCE_URL}else if("xlinkHref"===b||"form"===c&&"action"===b)return B.RESOURCE_URL}function pa(a,c,d,e,f){var g=oa(a,e),h=k[e]||f,l=b(d,!f,g,h);if(l){if("multiple"===e&&"select"===wa(a))throw fa("selmulti",ya(a));c.push({priority:100,compile:function(){return{pre:function(a,c,f){c=f.$$observers||(f.$$observers=V());if(m.test(e))throw fa("nodomevents");var k=f[e];k!==d&&(l=
k&&b(k,!0,g,h),d=k);l&&(f[e]=l(a),(c[e]||(c[e]=[])).$$inter=!0,(f.$$observers&&f.$$observers[e].$$scope||a).$watch(l,function(a,b){"class"===e&&a!==b?f.$updateClass(a,b):f.$set(e,a)}))}}}})}}function ga(a,b,c){var d=b[0],e=b.length,f=d.parentNode,g,h;if(a)for(g=0,h=a.length;g<h;g++)if(a[g]===d){a[g++]=c;h=g+e-1;for(var k=a.length;g<k;g++,h++)h<k?a[g]=a[h]:delete a[g];a.length-=e-1;a.context===d&&(a.context=c);break}f&&f.replaceChild(c,d);a=y.document.createDocumentFragment();for(g=0;g<e;g++)a.appendChild(b[g]);
F.hasData(d)&&(F.data(c,F.data(d)),F(d).off("$destroy"));F.cleanData(a.querySelectorAll("*"));for(g=1;g<e;g++)delete b[g];b[0]=c;b.length=1}function ra(a,b){return R(function(){return a.apply(null,arguments)},a,b)}function sa(a,b,d,e,f,g){try{a(b,d,e,f,g)}catch(h){c(h,ya(d))}}function la(a,c,d,e,f){function g(b,c,e){!C(d.$onChanges)||c===e||c!==c&&e!==e||(da||(a.$$postDigest(P),da=[]),m||(m={},da.push(h)),m[b]&&(e=m[b].previousValue),m[b]=new Hb(e,c))}function h(){d.$onChanges(m);m=void 0}var k=[],
l={},m;q(e,function(e,h){var m=e.attrName,p=e.optional,s,A,r,u;switch(e.mode){case "@":p||ua.call(c,m)||(d[h]=c[m]=void 0);p=c.$observe(m,function(a){if(D(a)||Ka(a))g(h,a,d[h]),d[h]=a});c.$$observers[m].$$scope=a;s=c[m];D(s)?d[h]=b(s)(a):Ka(s)&&(d[h]=s);l[h]=new Hb(ec,d[h]);k.push(p);break;case "=":if(!ua.call(c,m)){if(p)break;c[m]=void 0}if(p&&!c[m])break;A=n(c[m]);u=A.literal?na:function(a,b){return a===b||a!==a&&b!==b};r=A.assign||function(){s=d[h]=A(a);throw fa("nonassign",c[m],m,f.name);};s=
d[h]=A(a);p=function(b){u(b,d[h])||(u(b,s)?r(a,b=d[h]):d[h]=b);return s=b};p.$stateful=!0;p=e.collection?a.$watchCollection(c[m],p):a.$watch(n(c[m],p),null,A.literal);k.push(p);break;case "<":if(!ua.call(c,m)){if(p)break;c[m]=void 0}if(p&&!c[m])break;A=n(c[m]);var B=A.literal,M=d[h]=A(a);l[h]=new Hb(ec,d[h]);p=a.$watch(A,function(a,b){if(b===a){if(b===M||B&&na(b,M))return;b=M}g(h,a,b);d[h]=a},B);k.push(p);break;case "&":A=c.hasOwnProperty(m)?n(c[m]):w;if(A===w&&p)break;d[h]=function(b){return A(a,
b)}}});return{initialChanges:l,removeWatches:k.length&&function(){for(var a=0,b=k.length;a<b;++a)k[a]()}}}var za=/^\w/,ta=y.document.createElement("div"),Ea=u,Fa=p,xa=H,da;t.prototype={$normalize:Da,$addClass:function(a){a&&0<a.length&&T.addClass(this.$$element,a)},$removeClass:function(a){a&&0<a.length&&T.removeClass(this.$$element,a)},$updateClass:function(a,b){var c=fd(a,b);c&&c.length&&T.addClass(this.$$element,c);(c=fd(b,a))&&c.length&&T.removeClass(this.$$element,c)},$set:function(a,b,d,e){var f=
Zc(this.$$element[0],a),g=gd[a],h=a;f?(this.$$element.prop(a,b),e=f):g&&(this[g]=b,h=g);this[a]=b;e?this.$attr[a]=e:(e=this.$attr[a])||(this.$attr[a]=e=Hc(a,"-"));f=wa(this.$$element);if("a"===f&&("href"===a||"xlinkHref"===a)||"img"===f&&"src"===a)this[a]=b=S(b,"src"===a);else if("img"===f&&"srcset"===a&&x(b)){for(var f="",g=Y(b),k=/(\s+\d+x\s*,|\s+\d+w\s*,|\s+,|,\s+)/,k=/\s/.test(g)?k:/(,)/,g=g.split(k),k=Math.floor(g.length/2),l=0;l<k;l++)var m=2*l,f=f+S(Y(g[m]),!0),f=f+(" "+Y(g[m+1]));g=Y(g[2*
l]).split(/\s/);f+=S(Y(g[0]),!0);2===g.length&&(f+=" "+Y(g[1]));this[a]=b=f}!1!==d&&(null===b||z(b)?this.$$element.removeAttr(e):za.test(e)?this.$$element.attr(e,b):qa(this.$$element[0],e,b));(a=this.$$observers)&&q(a[h],function(a){try{a(b)}catch(d){c(d)}})},$observe:function(a,b){var c=this,d=c.$$observers||(c.$$observers=V()),e=d[a]||(d[a]=[]);e.push(b);J.$evalAsync(function(){e.$$inter||!c.hasOwnProperty(a)||z(c[a])||b(c[a])});return function(){bb(e,b)}}};var Aa=b.startSymbol(),Ba=b.endSymbol(),
Ca="{{"===Aa&&"}}"===Ba?$a:function(a){return a.replace(/\{\{/g,Aa).replace(/}}/g,Ba)},Ga=/^ngAttr[A-Z]/,Ha=/^(.+)Start$/;ca.$$addBindingInfo=r?function(a,b){var c=a.data("$binding")||[];I(b)?c=c.concat(b):c.push(b);a.data("$binding",c)}:w;ca.$$addBindingClass=r?function(a){Ja(a,"ng-binding")}:w;ca.$$addScopeInfo=r?function(a,b,c,d){a.data(c?d?"$isolateScopeNoTemplate":"$isolateScope":"$scope",b)}:w;ca.$$addScopeClass=r?function(a,b){Ja(a,b?"ng-isolate-scope":"ng-scope")}:w;ca.$$createComment=function(a,
b){var c="";r&&(c=" "+(a||"")+": ",b&&(c+=b+" "));return y.document.createComment(c)};return ca}]}function Hb(a,b){this.previousValue=a;this.currentValue=b}function Da(a){return hb(a.replace(bd,""))}function fd(a,b){var d="",c=a.split(/\s+/),f=b.split(/\s+/),e=0;a:for(;e<c.length;e++){for(var g=c[e],h=0;h<f.length;h++)if(g===f[h])continue a;d+=(0<d.length?" ":"")+g}return d}function ed(a){a=F(a);var b=a.length;if(1>=b)return a;for(;b--;){var d=a[b];(8===d.nodeType||d.nodeType===La&&""===d.nodeValue.trim())&&
pg.call(a,b,1)}return a}function ng(a,b){if(b&&D(b))return b;if(D(a)){var d=hd.exec(a);if(d)return d[3]}}function tf(){var a={},b=!1;this.has=function(b){return a.hasOwnProperty(b)};this.register=function(b,c){Ra(b,"controller");E(b)?R(a,b):a[b]=c};this.allowGlobals=function(){b=!0};this.$get=["$injector","$window",function(d,c){function f(a,b,c,d){if(!a||!E(a.$scope))throw G("$controller")("noscp",d,b);a.$scope[b]=c}return function(e,g,h,k){var l,m,n;h=!0===h;k&&D(k)&&(n=k);if(D(e)){k=e.match(hd);
if(!k)throw id("ctrlfmt",e);m=k[1];n=n||k[3];e=a.hasOwnProperty(m)?a[m]:Jc(g.$scope,m,!0)||(b?Jc(c,m,!0):void 0);if(!e)throw id("ctrlreg",m);Qa(e,m,!0)}if(h)return h=(I(e)?e[e.length-1]:e).prototype,l=Object.create(h||null),n&&f(g,n,l,m||e.name),R(function(){var a=d.invoke(e,l,g,m);a!==l&&(E(a)||C(a))&&(l=a,n&&f(g,n,l,m||e.name));return l},{instance:l,identifier:n});l=d.instantiate(e,g,m);n&&f(g,n,l,m||e.name);return l}}]}function uf(){this.$get=["$window",function(a){return F(a.document)}]}function vf(){this.$get=
["$log",function(a){return function(b,d){a.error.apply(a,arguments)}}]}function fc(a){return E(a)?ja(a)?a.toISOString():eb(a):a}function Af(){this.$get=function(){return function(a){if(!a)return"";var b=[];yc(a,function(a,c){null===a||z(a)||(I(a)?q(a,function(a){b.push(oa(c)+"="+oa(fc(a)))}):b.push(oa(c)+"="+oa(fc(a))))});return b.join("&")}}}function Bf(){this.$get=function(){return function(a){function b(a,f,e){null===a||z(a)||(I(a)?q(a,function(a,c){b(a,f+"["+(E(a)?c:"")+"]")}):E(a)&&!ja(a)?yc(a,
function(a,c){b(a,f+(e?"":"[")+c+(e?"":"]"))}):d.push(oa(f)+"="+oa(fc(a))))}if(!a)return"";var d=[];b(a,"",!0);return d.join("&")}}}function gc(a,b){if(D(a)){var d=a.replace(qg,"").trim();if(d){var c=b("Content-Type");(c=c&&0===c.indexOf(jd))||(c=(c=d.match(rg))&&sg[c[0]].test(d));c&&(a=Cc(d))}}return a}function kd(a){var b=V(),d;D(a)?q(a.split("\n"),function(a){d=a.indexOf(":");var f=Q(Y(a.substr(0,d)));a=Y(a.substr(d+1));f&&(b[f]=b[f]?b[f]+", "+a:a)}):E(a)&&q(a,function(a,d){var e=Q(d),g=Y(a);e&&
(b[e]=b[e]?b[e]+", "+g:g)});return b}function ld(a){var b;return function(d){b||(b=kd(a));return d?(d=b[Q(d)],void 0===d&&(d=null),d):b}}function md(a,b,d,c){if(C(c))return c(a,b,d);q(c,function(c){a=c(a,b,d)});return a}function zf(){var a=this.defaults={transformResponse:[gc],transformRequest:[function(a){return E(a)&&"[object File]"!==ma.call(a)&&"[object Blob]"!==ma.call(a)&&"[object FormData]"!==ma.call(a)?eb(a):a}],headers:{common:{Accept:"application/json, text/plain, */*"},post:ka(hc),put:ka(hc),
patch:ka(hc)},xsrfCookieName:"XSRF-TOKEN",xsrfHeaderName:"X-XSRF-TOKEN",paramSerializer:"$httpParamSerializer"},b=!1;this.useApplyAsync=function(a){return x(a)?(b=!!a,this):b};var d=!0;this.useLegacyPromiseExtensions=function(a){return x(a)?(d=!!a,this):d};var c=this.interceptors=[];this.$get=["$httpBackend","$$cookieReader","$cacheFactory","$rootScope","$q","$injector",function(f,e,g,h,k,l){function m(b){function c(a,b){for(var d=0,e=b.length;d<e;){var f=b[d++],g=b[d++];a=a.then(f,g)}b.length=0;
return a}function e(a,b){var c,d={};q(a,function(a,e){C(a)?(c=a(b),null!=c&&(d[e]=c)):d[e]=a});return d}function f(a){var b=R({},a);b.data=md(a.data,a.headers,a.status,g.transformResponse);a=a.status;return 200<=a&&300>a?b:k.reject(b)}if(!E(b))throw G("$http")("badreq",b);if(!D(b.url))throw G("$http")("badreq",b.url);var g=R({method:"get",transformRequest:a.transformRequest,transformResponse:a.transformResponse,paramSerializer:a.paramSerializer},b);g.headers=function(b){var c=a.headers,d=R({},b.headers),
f,g,h,c=R({},c.common,c[Q(b.method)]);a:for(f in c){g=Q(f);for(h in d)if(Q(h)===g)continue a;d[f]=c[f]}return e(d,ka(b))}(b);g.method=wb(g.method);g.paramSerializer=D(g.paramSerializer)?l.get(g.paramSerializer):g.paramSerializer;var h=[],m=[],s=k.when(g);q(H,function(a){(a.request||a.requestError)&&h.unshift(a.request,a.requestError);(a.response||a.responseError)&&m.push(a.response,a.responseError)});s=c(s,h);s=s.then(function(b){var c=b.headers,d=md(b.data,ld(c),void 0,b.transformRequest);z(d)&&
q(c,function(a,b){"content-type"===Q(b)&&delete c[b]});z(b.withCredentials)&&!z(a.withCredentials)&&(b.withCredentials=a.withCredentials);return n(b,d).then(f,f)});s=c(s,m);d?(s.success=function(a){Qa(a,"fn");s.then(function(b){a(b.data,b.status,b.headers,g)});return s},s.error=function(a){Qa(a,"fn");s.then(null,function(b){a(b.data,b.status,b.headers,g)});return s}):(s.success=nd("success"),s.error=nd("error"));return s}function n(c,d){function g(a){if(a){var c={};q(a,function(a,d){c[d]=function(c){function d(){a(c)}
b?h.$applyAsync(d):h.$$phase?d():h.$apply(d)}});return c}}function l(a,c,d,e){function f(){n(c,a,d,e)}J&&(200<=a&&300>a?J.put(S,[a,c,kd(d),e]):J.remove(S));b?h.$applyAsync(f):(f(),h.$$phase||h.$apply())}function n(a,b,d,e){b=-1<=b?b:0;(200<=b&&300>b?O.resolve:O.reject)({data:a,status:b,headers:ld(d),config:c,statusText:e})}function H(a){n(a.data,a.status,ka(a.headers()),a.statusText)}function L(){var a=m.pendingRequests.indexOf(c);-1!==a&&m.pendingRequests.splice(a,1)}var O=k.defer(),M=O.promise,
J,B,T=c.headers,S=r(c.url,c.paramSerializer(c.params));m.pendingRequests.push(c);M.then(L,L);!c.cache&&!a.cache||!1===c.cache||"GET"!==c.method&&"JSONP"!==c.method||(J=E(c.cache)?c.cache:E(a.cache)?a.cache:s);J&&(B=J.get(S),x(B)?B&&C(B.then)?B.then(H,H):I(B)?n(B[1],B[0],ka(B[2]),B[3]):n(B,200,{},"OK"):J.put(S,M));z(B)&&((B=od(c.url)?e()[c.xsrfCookieName||a.xsrfCookieName]:void 0)&&(T[c.xsrfHeaderName||a.xsrfHeaderName]=B),f(c.method,S,d,l,T,c.timeout,c.withCredentials,c.responseType,g(c.eventHandlers),
g(c.uploadEventHandlers)));return M}function r(a,b){0<b.length&&(a+=(-1===a.indexOf("?")?"?":"&")+b);return a}var s=g("$http");a.paramSerializer=D(a.paramSerializer)?l.get(a.paramSerializer):a.paramSerializer;var H=[];q(c,function(a){H.unshift(D(a)?l.get(a):l.invoke(a))});m.pendingRequests=[];(function(a){q(arguments,function(a){m[a]=function(b,c){return m(R({},c||{},{method:a,url:b}))}})})("get","delete","head","jsonp");(function(a){q(arguments,function(a){m[a]=function(b,c,d){return m(R({},d||{},
{method:a,url:b,data:c}))}})})("post","put","patch");m.defaults=a;return m}]}function Df(){this.$get=function(){return function(){return new y.XMLHttpRequest}}}function Cf(){this.$get=["$browser","$jsonpCallbacks","$document","$xhrFactory",function(a,b,d,c){return tg(a,c,a.defer,b,d[0])}]}function tg(a,b,d,c,f){function e(a,b,d){a=a.replace("JSON_CALLBACK",b);var e=f.createElement("script"),m=null;e.type="text/javascript";e.src=a;e.async=!0;m=function(a){e.removeEventListener("load",m,!1);e.removeEventListener("error",
m,!1);f.body.removeChild(e);e=null;var g=-1,s="unknown";a&&("load"!==a.type||c.wasCalled(b)||(a={type:"error"}),s=a.type,g="error"===a.type?404:200);d&&d(g,s)};e.addEventListener("load",m,!1);e.addEventListener("error",m,!1);f.body.appendChild(e);return m}return function(f,h,k,l,m,n,r,s,H,u){function p(){v&&v();N&&N.abort()}function K(b,c,e,f,g){x(O)&&d.cancel(O);v=N=null;b(c,e,f,g);a.$$completeOutstandingRequest(w)}a.$$incOutstandingRequestCount();h=h||a.url();if("jsonp"===Q(f))var A=c.createCallback(h),
v=e(h,A,function(a,b){var d=200===a&&c.getResponse(A);K(l,a,d,"",b);c.removeCallback(A)});else{var N=b(f,h);N.open(f,h,!0);q(m,function(a,b){x(a)&&N.setRequestHeader(b,a)});N.onload=function(){var a=N.statusText||"",b="response"in N?N.response:N.responseText,c=1223===N.status?204:N.status;0===c&&(c=b?200:"file"===ta(h).protocol?404:0);K(l,c,b,N.getAllResponseHeaders(),a)};f=function(){K(l,-1,null,null,"")};N.onerror=f;N.onabort=f;N.ontimeout=f;q(H,function(a,b){N.addEventListener(b,a)});q(u,function(a,
b){N.upload.addEventListener(b,a)});r&&(N.withCredentials=!0);if(s)try{N.responseType=s}catch(L){if("json"!==s)throw L;}N.send(z(k)?null:k)}if(0<n)var O=d(p,n);else n&&C(n.then)&&n.then(p)}}function xf(){var a="{{",b="}}";this.startSymbol=function(b){return b?(a=b,this):a};this.endSymbol=function(a){return a?(b=a,this):b};this.$get=["$parse","$exceptionHandler","$sce",function(d,c,f){function e(a){return"\\\\\\"+a}function g(c){return c.replace(n,a).replace(r,b)}function h(a,b,c,d){var e=a.$watch(function(a){e();
return d(a)},b,c);return e}function k(e,k,n,p){function r(a){try{var b=a;a=n?f.getTrusted(n,b):f.valueOf(b);var d;if(p&&!x(a))d=a;else if(null==a)d="";else{switch(typeof a){case "string":break;case "number":a=""+a;break;default:a=eb(a)}d=a}return d}catch(g){c(Ha.interr(e,g))}}if(!e.length||-1===e.indexOf(a)){var A;k||(k=g(e),A=ha(k),A.exp=e,A.expressions=[],A.$$watchDelegate=h);return A}p=!!p;var v,q,L=0,O=[],M=[];A=e.length;for(var J=[],B=[];L<A;)if(-1!==(v=e.indexOf(a,L))&&-1!==(q=e.indexOf(b,v+
l)))L!==v&&J.push(g(e.substring(L,v))),L=e.substring(v+l,q),O.push(L),M.push(d(L,r)),L=q+m,B.push(J.length),J.push("");else{L!==A&&J.push(g(e.substring(L)));break}n&&1<J.length&&Ha.throwNoconcat(e);if(!k||O.length){var T=function(a){for(var b=0,c=O.length;b<c;b++){if(p&&z(a[b]))return;J[B[b]]=a[b]}return J.join("")};return R(function(a){var b=0,d=O.length,f=Array(d);try{for(;b<d;b++)f[b]=M[b](a);return T(f)}catch(g){c(Ha.interr(e,g))}},{exp:e,expressions:O,$$watchDelegate:function(a,b){var c;return a.$watchGroup(M,
function(d,e){var f=T(d);C(b)&&b.call(this,f,d!==e?c:f,a);c=f})}})}}var l=a.length,m=b.length,n=new RegExp(a.replace(/./g,e),"g"),r=new RegExp(b.replace(/./g,e),"g");k.startSymbol=function(){return a};k.endSymbol=function(){return b};return k}]}function yf(){this.$get=["$rootScope","$window","$q","$$q","$browser",function(a,b,d,c,f){function e(e,k,l,m){function n(){r?e.apply(null,s):e(p)}var r=4<arguments.length,s=r?va.call(arguments,4):[],H=b.setInterval,u=b.clearInterval,p=0,K=x(m)&&!m,A=(K?c:d).defer(),
v=A.promise;l=x(l)?l:0;v.$$intervalId=H(function(){K?f.defer(n):a.$evalAsync(n);A.notify(p++);0<l&&p>=l&&(A.resolve(p),u(v.$$intervalId),delete g[v.$$intervalId]);K||a.$apply()},k);g[v.$$intervalId]=A;return v}var g={};e.cancel=function(a){return a&&a.$$intervalId in g?(g[a.$$intervalId].reject("canceled"),b.clearInterval(a.$$intervalId),delete g[a.$$intervalId],!0):!1};return e}]}function ic(a){a=a.split("/");for(var b=a.length;b--;)a[b]=tb(a[b]);return a.join("/")}function pd(a,b){var d=ta(a);b.$$protocol=
d.protocol;b.$$host=d.hostname;b.$$port=Z(d.port)||ug[d.protocol]||null}function qd(a,b){if(vg.test(a))throw lb("badpath",a);var d="/"!==a.charAt(0);d&&(a="/"+a);var c=ta(a);b.$$path=decodeURIComponent(d&&"/"===c.pathname.charAt(0)?c.pathname.substring(1):c.pathname);b.$$search=Fc(c.search);b.$$hash=decodeURIComponent(c.hash);b.$$path&&"/"!==b.$$path.charAt(0)&&(b.$$path="/"+b.$$path)}function ra(a,b){if(b.slice(0,a.length)===a)return b.substr(a.length)}function Ga(a){var b=a.indexOf("#");return-1===
b?a:a.substr(0,b)}function mb(a){return a.replace(/(#.+)|#$/,"$1")}function jc(a,b,d){this.$$html5=!0;d=d||"";pd(a,this);this.$$parse=function(a){var d=ra(b,a);if(!D(d))throw lb("ipthprfx",a,b);qd(d,this);this.$$path||(this.$$path="/");this.$$compose()};this.$$compose=function(){var a=Vb(this.$$search),d=this.$$hash?"#"+tb(this.$$hash):"";this.$$url=ic(this.$$path)+(a?"?"+a:"")+d;this.$$absUrl=b+this.$$url.substr(1)};this.$$parseLinkUrl=function(c,f){if(f&&"#"===f[0])return this.hash(f.slice(1)),
!0;var e,g;x(e=ra(a,c))?(g=e,g=d&&x(e=ra(d,e))?b+(ra("/",e)||e):a+g):x(e=ra(b,c))?g=b+e:b===c+"/"&&(g=b);g&&this.$$parse(g);return!!g}}function kc(a,b,d){pd(a,this);this.$$parse=function(c){var f=ra(a,c)||ra(b,c),e;z(f)||"#"!==f.charAt(0)?this.$$html5?e=f:(e="",z(f)&&(a=c,this.replace())):(e=ra(d,f),z(e)&&(e=f));qd(e,this);c=this.$$path;var f=a,g=/^\/[A-Z]:(\/.*)/;e.slice(0,f.length)===f&&(e=e.replace(f,""));g.exec(e)||(c=(e=g.exec(c))?e[1]:c);this.$$path=c;this.$$compose()};this.$$compose=function(){var b=
Vb(this.$$search),f=this.$$hash?"#"+tb(this.$$hash):"";this.$$url=ic(this.$$path)+(b?"?"+b:"")+f;this.$$absUrl=a+(this.$$url?d+this.$$url:"")};this.$$parseLinkUrl=function(b,d){return Ga(a)===Ga(b)?(this.$$parse(b),!0):!1}}function rd(a,b,d){this.$$html5=!0;kc.apply(this,arguments);this.$$parseLinkUrl=function(c,f){if(f&&"#"===f[0])return this.hash(f.slice(1)),!0;var e,g;a===Ga(c)?e=c:(g=ra(b,c))?e=a+d+g:b===c+"/"&&(e=b);e&&this.$$parse(e);return!!e};this.$$compose=function(){var b=Vb(this.$$search),
f=this.$$hash?"#"+tb(this.$$hash):"";this.$$url=ic(this.$$path)+(b?"?"+b:"")+f;this.$$absUrl=a+d+this.$$url}}function Ib(a){return function(){return this[a]}}function sd(a,b){return function(d){if(z(d))return this[a];this[a]=b(d);this.$$compose();return this}}function Ff(){var a="",b={enabled:!1,requireBase:!0,rewriteLinks:!0};this.hashPrefix=function(b){return x(b)?(a=b,this):a};this.html5Mode=function(a){if(Ka(a))return b.enabled=a,this;if(E(a)){Ka(a.enabled)&&(b.enabled=a.enabled);Ka(a.requireBase)&&
(b.requireBase=a.requireBase);if(Ka(a.rewriteLinks)||D(a.rewriteLinks))b.rewriteLinks=a.rewriteLinks;return this}return b};this.$get=["$rootScope","$browser","$sniffer","$rootElement","$window",function(d,c,f,e,g){function h(a,b,d){var e=l.url(),f=l.$$state;try{c.url(a,b,d),l.$$state=c.state()}catch(g){throw l.url(e),l.$$state=f,g;}}function k(a,b){d.$broadcast("$locationChangeSuccess",l.absUrl(),a,l.$$state,b)}var l,m;m=c.baseHref();var n=c.url(),r;if(b.enabled){if(!m&&b.requireBase)throw lb("nobase");
r=n.substring(0,n.indexOf("/",n.indexOf("//")+2))+(m||"/");m=f.history?jc:rd}else r=Ga(n),m=kc;var s=r.substr(0,Ga(r).lastIndexOf("/")+1);l=new m(r,s,"#"+a);l.$$parseLinkUrl(n,n);l.$$state=c.state();var H=/^\s*(javascript|mailto):/i;e.on("click",function(a){var f=b.rewriteLinks;if(f&&!a.ctrlKey&&!a.metaKey&&!a.shiftKey&&2!==a.which&&2!==a.button){for(var h=F(a.target);"a"!==wa(h[0]);)if(h[0]===e[0]||!(h=h.parent())[0])return;if(!D(f)||!z(h.attr(f))){var f=h.prop("href"),k=h.attr("href")||h.attr("xlink:href");
E(f)&&"[object SVGAnimatedString]"===f.toString()&&(f=ta(f.animVal).href);H.test(f)||!f||h.attr("target")||a.isDefaultPrevented()||!l.$$parseLinkUrl(f,k)||(a.preventDefault(),l.absUrl()!==c.url()&&(d.$apply(),g.angular["ff-684208-preventDefault"]=!0))}}});mb(l.absUrl())!==mb(n)&&c.url(l.absUrl(),!0);var u=!0;c.onUrlChange(function(a,b){z(ra(s,a))?g.location.href=a:(d.$evalAsync(function(){var c=l.absUrl(),e=l.$$state,f;a=mb(a);l.$$parse(a);l.$$state=b;f=d.$broadcast("$locationChangeStart",a,c,b,e).defaultPrevented;
l.absUrl()===a&&(f?(l.$$parse(c),l.$$state=e,h(c,!1,e)):(u=!1,k(c,e)))}),d.$$phase||d.$digest())});d.$watch(function(){var a=mb(c.url()),b=mb(l.absUrl()),e=c.state(),g=l.$$replace,m=a!==b||l.$$html5&&f.history&&e!==l.$$state;if(u||m)u=!1,d.$evalAsync(function(){var b=l.absUrl(),c=d.$broadcast("$locationChangeStart",b,a,l.$$state,e).defaultPrevented;l.absUrl()===b&&(c?(l.$$parse(a),l.$$state=e):(m&&h(b,g,e===l.$$state?null:l.$$state),k(a,e)))});l.$$replace=!1});return l}]}function Gf(){var a=!0,b=
this;this.debugEnabled=function(b){return x(b)?(a=b,this):a};this.$get=["$window",function(d){function c(a){a instanceof Error&&(a.stack?a=a.message&&-1===a.stack.indexOf(a.message)?"Error: "+a.message+"\n"+a.stack:a.stack:a.sourceURL&&(a=a.message+"\n"+a.sourceURL+":"+a.line));return a}function f(a){var b=d.console||{},f=b[a]||b.log||w;a=!1;try{a=!!f.apply}catch(k){}return a?function(){var a=[];q(arguments,function(b){a.push(c(b))});return f.apply(b,a)}:function(a,b){f(a,null==b?"":b)}}return{log:f("log"),
info:f("info"),warn:f("warn"),error:f("error"),debug:function(){var c=f("debug");return function(){a&&c.apply(b,arguments)}}()}}]}function Ua(a,b){if("__defineGetter__"===a||"__defineSetter__"===a||"__lookupGetter__"===a||"__lookupSetter__"===a||"__proto__"===a)throw ea("isecfld",b);return a}function wg(a){return a+""}function Ea(a,b){if(a){if(a.constructor===a)throw ea("isecfn",b);if(a.window===a)throw ea("isecwindow",b);if(a.children&&(a.nodeName||a.prop&&a.attr&&a.find))throw ea("isecdom",b);if(a===
Object)throw ea("isecobj",b);}return a}function td(a,b){if(a){if(a.constructor===a)throw ea("isecfn",b);if(a===xg||a===yg||a===zg)throw ea("isecff",b);}}function Jb(a,b){if(a&&(a===ud||a===vd||a===wd||a===xd||a===yd||a===zd||a===Ag||a===Bg||a===Kb||a===Cg||a===Ad||a===Dg))throw ea("isecaf",b);}function Eg(a,b){return"undefined"!==typeof a?a:b}function Bd(a,b){return"undefined"===typeof a?b:"undefined"===typeof b?a:a+b}function X(a,b){var d,c,f;switch(a.type){case t.Program:d=!0;q(a.body,function(a){X(a.expression,
b);d=d&&a.expression.constant});a.constant=d;break;case t.Literal:a.constant=!0;a.toWatch=[];break;case t.UnaryExpression:X(a.argument,b);a.constant=a.argument.constant;a.toWatch=a.argument.toWatch;break;case t.BinaryExpression:X(a.left,b);X(a.right,b);a.constant=a.left.constant&&a.right.constant;a.toWatch=a.left.toWatch.concat(a.right.toWatch);break;case t.LogicalExpression:X(a.left,b);X(a.right,b);a.constant=a.left.constant&&a.right.constant;a.toWatch=a.constant?[]:[a];break;case t.ConditionalExpression:X(a.test,
b);X(a.alternate,b);X(a.consequent,b);a.constant=a.test.constant&&a.alternate.constant&&a.consequent.constant;a.toWatch=a.constant?[]:[a];break;case t.Identifier:a.constant=!1;a.toWatch=[a];break;case t.MemberExpression:X(a.object,b);a.computed&&X(a.property,b);a.constant=a.object.constant&&(!a.computed||a.property.constant);a.toWatch=[a];break;case t.CallExpression:d=f=a.filter?!b(a.callee.name).$stateful:!1;c=[];q(a.arguments,function(a){X(a,b);d=d&&a.constant;a.constant||c.push.apply(c,a.toWatch)});
a.constant=d;a.toWatch=f?c:[a];break;case t.AssignmentExpression:X(a.left,b);X(a.right,b);a.constant=a.left.constant&&a.right.constant;a.toWatch=[a];break;case t.ArrayExpression:d=!0;c=[];q(a.elements,function(a){X(a,b);d=d&&a.constant;a.constant||c.push.apply(c,a.toWatch)});a.constant=d;a.toWatch=c;break;case t.ObjectExpression:d=!0;c=[];q(a.properties,function(a){X(a.value,b);d=d&&a.value.constant&&!a.computed;a.value.constant||c.push.apply(c,a.value.toWatch)});a.constant=d;a.toWatch=c;break;case t.ThisExpression:a.constant=
!1;a.toWatch=[];break;case t.LocalsExpression:a.constant=!1,a.toWatch=[]}}function Cd(a){if(1===a.length){a=a[0].expression;var b=a.toWatch;return 1!==b.length?b:b[0]!==a?b:void 0}}function Dd(a){return a.type===t.Identifier||a.type===t.MemberExpression}function Ed(a){if(1===a.body.length&&Dd(a.body[0].expression))return{type:t.AssignmentExpression,left:a.body[0].expression,right:{type:t.NGValueParameter},operator:"="}}function Fd(a){return 0===a.body.length||1===a.body.length&&(a.body[0].expression.type===
t.Literal||a.body[0].expression.type===t.ArrayExpression||a.body[0].expression.type===t.ObjectExpression)}function Gd(a,b){this.astBuilder=a;this.$filter=b}function Hd(a,b){this.astBuilder=a;this.$filter=b}function Lb(a){return"constructor"===a}function lc(a){return C(a.valueOf)?a.valueOf():Fg.call(a)}function Hf(){var a=V(),b=V(),d={"true":!0,"false":!1,"null":null,undefined:void 0},c,f;this.addLiteral=function(a,b){d[a]=b};this.setIdentifierFns=function(a,b){c=a;f=b;return this};this.$get=["$filter",
function(e){function g(c,d,f){var g,k,H;f=f||K;switch(typeof c){case "string":H=c=c.trim();var q=f?b:a;g=q[H];if(!g){":"===c.charAt(0)&&":"===c.charAt(1)&&(k=!0,c=c.substring(2));g=f?p:u;var B=new mc(g);g=(new nc(B,e,g)).parse(c);g.constant?g.$$watchDelegate=r:k?g.$$watchDelegate=g.literal?n:m:g.inputs&&(g.$$watchDelegate=l);f&&(g=h(g));q[H]=g}return s(g,d);case "function":return s(c,d);default:return s(w,d)}}function h(a){function b(c,d,e,f){var g=K;K=!0;try{return a(c,d,e,f)}finally{K=g}}if(!a)return a;
b.$$watchDelegate=a.$$watchDelegate;b.assign=h(a.assign);b.constant=a.constant;b.literal=a.literal;for(var c=0;a.inputs&&c<a.inputs.length;++c)a.inputs[c]=h(a.inputs[c]);b.inputs=a.inputs;return b}function k(a,b){return null==a||null==b?a===b:"object"===typeof a&&(a=lc(a),"object"===typeof a)?!1:a===b||a!==a&&b!==b}function l(a,b,c,d,e){var f=d.inputs,g;if(1===f.length){var h=k,f=f[0];return a.$watch(function(a){var b=f(a);k(b,h)||(g=d(a,void 0,void 0,[b]),h=b&&lc(b));return g},b,c,e)}for(var l=[],
m=[],n=0,s=f.length;n<s;n++)l[n]=k,m[n]=null;return a.$watch(function(a){for(var b=!1,c=0,e=f.length;c<e;c++){var h=f[c](a);if(b||(b=!k(h,l[c])))m[c]=h,l[c]=h&&lc(h)}b&&(g=d(a,void 0,void 0,m));return g},b,c,e)}function m(a,b,c,d){var e,f;return e=a.$watch(function(a){return d(a)},function(a,c,d){f=a;C(b)&&b.apply(this,arguments);x(a)&&d.$$postDigest(function(){x(f)&&e()})},c)}function n(a,b,c,d){function e(a){var b=!0;q(a,function(a){x(a)||(b=!1)});return b}var f,g;return f=a.$watch(function(a){return d(a)},
function(a,c,d){g=a;C(b)&&b.call(this,a,c,d);e(a)&&d.$$postDigest(function(){e(g)&&f()})},c)}function r(a,b,c,d){var e=a.$watch(function(a){e();return d(a)},b,c);return e}function s(a,b){if(!b)return a;var c=a.$$watchDelegate,d=!1,c=c!==n&&c!==m?function(c,e,f,g){f=d&&g?g[0]:a(c,e,f,g);return b(f,c,e)}:function(c,d,e,f){e=a(c,d,e,f);c=b(e,c,d);return x(e)?c:e};a.$$watchDelegate&&a.$$watchDelegate!==l?c.$$watchDelegate=a.$$watchDelegate:b.$stateful||(c.$$watchDelegate=l,d=!a.inputs,c.inputs=a.inputs?
a.inputs:[a]);return c}var H=da().noUnsafeEval,u={csp:H,expensiveChecks:!1,literals:sa(d),isIdentifierStart:C(c)&&c,isIdentifierContinue:C(f)&&f},p={csp:H,expensiveChecks:!0,literals:sa(d),isIdentifierStart:C(c)&&c,isIdentifierContinue:C(f)&&f},K=!1;g.$$runningExpensiveChecks=function(){return K};return g}]}function Jf(){this.$get=["$rootScope","$exceptionHandler",function(a,b){return Id(function(b){a.$evalAsync(b)},b)}]}function Kf(){this.$get=["$browser","$exceptionHandler",function(a,b){return Id(function(b){a.defer(b)},
b)}]}function Id(a,b){function d(){var a=new g;a.resolve=f(a,a.resolve);a.reject=f(a,a.reject);a.notify=f(a,a.notify);return a}function c(){this.$$state={status:0}}function f(a,b){return function(c){b.call(a,c)}}function e(c){!c.processScheduled&&c.pending&&(c.processScheduled=!0,a(function(){var a,d,e;e=c.pending;c.processScheduled=!1;c.pending=void 0;for(var f=0,g=e.length;f<g;++f){d=e[f][0];a=e[f][c.status];try{C(a)?d.resolve(a(c.value)):1===c.status?d.resolve(c.value):d.reject(c.value)}catch(h){d.reject(h),
b(h)}}}))}function g(){this.promise=new c}function h(a){var b=new g;b.reject(a);return b.promise}function k(a,b,c){var d=null;try{C(c)&&(d=c())}catch(e){return h(e)}return d&&C(d.then)?d.then(function(){return b(a)},h):b(a)}function l(a,b,c,d){var e=new g;e.resolve(a);return e.promise.then(b,c,d)}function m(a){if(!C(a))throw n("norslvr",a);var b=new g;a(function(a){b.resolve(a)},function(a){b.reject(a)});return b.promise}var n=G("$q",TypeError);R(c.prototype,{then:function(a,b,c){if(z(a)&&z(b)&&z(c))return this;
var d=new g;this.$$state.pending=this.$$state.pending||[];this.$$state.pending.push([d,a,b,c]);0<this.$$state.status&&e(this.$$state);return d.promise},"catch":function(a){return this.then(null,a)},"finally":function(a,b){return this.then(function(b){return k(b,r,a)},function(b){return k(b,h,a)},b)}});R(g.prototype,{resolve:function(a){this.promise.$$state.status||(a===this.promise?this.$$reject(n("qcycle",a)):this.$$resolve(a))},$$resolve:function(a){function c(a){k||(k=!0,h.$$resolve(a))}function d(a){k||
(k=!0,h.$$reject(a))}var g,h=this,k=!1;try{if(E(a)||C(a))g=a&&a.then;C(g)?(this.promise.$$state.status=-1,g.call(a,c,d,f(this,this.notify))):(this.promise.$$state.value=a,this.promise.$$state.status=1,e(this.promise.$$state))}catch(l){d(l),b(l)}},reject:function(a){this.promise.$$state.status||this.$$reject(a)},$$reject:function(a){this.promise.$$state.value=a;this.promise.$$state.status=2;e(this.promise.$$state)},notify:function(c){var d=this.promise.$$state.pending;0>=this.promise.$$state.status&&
d&&d.length&&a(function(){for(var a,e,f=0,g=d.length;f<g;f++){e=d[f][0];a=d[f][3];try{e.notify(C(a)?a(c):c)}catch(h){b(h)}}})}});var r=l;m.prototype=c.prototype;m.defer=d;m.reject=h;m.when=l;m.resolve=r;m.all=function(a){var b=new g,c=0,d=I(a)?[]:{};q(a,function(a,e){c++;l(a).then(function(a){d[e]=a;--c||b.resolve(d)},function(a){b.reject(a)})});0===c&&b.resolve(d);return b.promise};m.race=function(a){var b=d();q(a,function(a){l(a).then(b.resolve,b.reject)});return b.promise};return m}function Tf(){this.$get=
["$window","$timeout",function(a,b){var d=a.requestAnimationFrame||a.webkitRequestAnimationFrame,c=a.cancelAnimationFrame||a.webkitCancelAnimationFrame||a.webkitCancelRequestAnimationFrame,f=!!d,e=f?function(a){var b=d(a);return function(){c(b)}}:function(a){var c=b(a,16.66,!1);return function(){b.cancel(c)}};e.supported=f;return e}]}function If(){function a(a){function b(){this.$$watchers=this.$$nextSibling=this.$$childHead=this.$$childTail=null;this.$$listeners={};this.$$listenerCount={};this.$$watchersCount=
0;this.$id=++sb;this.$$ChildScope=null}b.prototype=a;return b}var b=10,d=G("$rootScope"),c=null,f=null;this.digestTtl=function(a){arguments.length&&(b=a);return b};this.$get=["$exceptionHandler","$parse","$browser",function(e,g,h){function k(a){a.currentScope.$$destroyed=!0}function l(a){9===Ia&&(a.$$childHead&&l(a.$$childHead),a.$$nextSibling&&l(a.$$nextSibling));a.$parent=a.$$nextSibling=a.$$prevSibling=a.$$childHead=a.$$childTail=a.$root=a.$$watchers=null}function m(){this.$id=++sb;this.$$phase=
this.$parent=this.$$watchers=this.$$nextSibling=this.$$prevSibling=this.$$childHead=this.$$childTail=null;this.$root=this;this.$$destroyed=!1;this.$$listeners={};this.$$listenerCount={};this.$$watchersCount=0;this.$$isolateBindings=null}function n(a){if(K.$$phase)throw d("inprog",K.$$phase);K.$$phase=a}function r(a,b){do a.$$watchersCount+=b;while(a=a.$parent)}function s(a,b,c){do a.$$listenerCount[c]-=b,0===a.$$listenerCount[c]&&delete a.$$listenerCount[c];while(a=a.$parent)}function H(){}function u(){for(;t.length;)try{t.shift()()}catch(a){e(a)}f=
null}function p(){null===f&&(f=h.defer(function(){K.$apply(u)}))}m.prototype={constructor:m,$new:function(b,c){var d;c=c||this;b?(d=new m,d.$root=this.$root):(this.$$ChildScope||(this.$$ChildScope=a(this)),d=new this.$$ChildScope);d.$parent=c;d.$$prevSibling=c.$$childTail;c.$$childHead?(c.$$childTail.$$nextSibling=d,c.$$childTail=d):c.$$childHead=c.$$childTail=d;(b||c!==this)&&d.$on("$destroy",k);return d},$watch:function(a,b,d,e){var f=g(a);if(f.$$watchDelegate)return f.$$watchDelegate(this,b,d,
f,a);var h=this,k=h.$$watchers,l={fn:b,last:H,get:f,exp:e||a,eq:!!d};c=null;C(b)||(l.fn=w);k||(k=h.$$watchers=[],k.$$digestWatchIndex=-1);k.unshift(l);k.$$digestWatchIndex++;r(this,1);return function(){var a=bb(k,l);0<=a&&(r(h,-1),a<k.$$digestWatchIndex&&k.$$digestWatchIndex--);c=null}},$watchGroup:function(a,b){function c(){h=!1;k?(k=!1,b(e,e,g)):b(e,d,g)}var d=Array(a.length),e=Array(a.length),f=[],g=this,h=!1,k=!0;if(!a.length){var l=!0;g.$evalAsync(function(){l&&b(e,e,g)});return function(){l=
!1}}if(1===a.length)return this.$watch(a[0],function(a,c,f){e[0]=a;d[0]=c;b(e,a===c?e:d,f)});q(a,function(a,b){var k=g.$watch(a,function(a,f){e[b]=a;d[b]=f;h||(h=!0,g.$evalAsync(c))});f.push(k)});return function(){for(;f.length;)f.shift()()}},$watchCollection:function(a,b){function c(a){e=a;var b,d,g,h;if(!z(e)){if(E(e))if(la(e))for(f!==n&&(f=n,s=f.length=0,l++),a=e.length,s!==a&&(l++,f.length=s=a),b=0;b<a;b++)h=f[b],g=e[b],d=h!==h&&g!==g,d||h===g||(l++,f[b]=g);else{f!==r&&(f=r={},s=0,l++);a=0;for(b in e)ua.call(e,
b)&&(a++,g=e[b],h=f[b],b in f?(d=h!==h&&g!==g,d||h===g||(l++,f[b]=g)):(s++,f[b]=g,l++));if(s>a)for(b in l++,f)ua.call(e,b)||(s--,delete f[b])}else f!==e&&(f=e,l++);return l}}c.$stateful=!0;var d=this,e,f,h,k=1<b.length,l=0,m=g(a,c),n=[],r={},p=!0,s=0;return this.$watch(m,function(){p?(p=!1,b(e,e,d)):b(e,h,d);if(k)if(E(e))if(la(e)){h=Array(e.length);for(var a=0;a<e.length;a++)h[a]=e[a]}else for(a in h={},e)ua.call(e,a)&&(h[a]=e[a]);else h=e})},$digest:function(){var a,g,k,l,m,r,p,s=b,q,t=[],N,x;n("$digest");
h.$$checkUrlChange();this===K&&null!==f&&(h.defer.cancel(f),u());c=null;do{p=!1;q=this;for(r=0;r<A.length;r++){try{x=A[r],x.scope.$eval(x.expression,x.locals)}catch(z){e(z)}c=null}A.length=0;a:do{if(r=q.$$watchers)for(r.$$digestWatchIndex=r.length;r.$$digestWatchIndex--;)try{if(a=r[r.$$digestWatchIndex])if(m=a.get,(g=m(q))!==(k=a.last)&&!(a.eq?na(g,k):ia(g)&&ia(k)))p=!0,c=a,a.last=a.eq?sa(g,null):g,l=a.fn,l(g,k===H?g:k,q),5>s&&(N=4-s,t[N]||(t[N]=[]),t[N].push({msg:C(a.exp)?"fn: "+(a.exp.name||a.exp.toString()):
a.exp,newVal:g,oldVal:k}));else if(a===c){p=!1;break a}}catch(w){e(w)}if(!(r=q.$$watchersCount&&q.$$childHead||q!==this&&q.$$nextSibling))for(;q!==this&&!(r=q.$$nextSibling);)q=q.$parent}while(q=r);if((p||A.length)&&!s--)throw K.$$phase=null,d("infdig",b,t);}while(p||A.length);for(K.$$phase=null;L<v.length;)try{v[L++]()}catch(y){e(y)}v.length=L=0},$destroy:function(){if(!this.$$destroyed){var a=this.$parent;this.$broadcast("$destroy");this.$$destroyed=!0;this===K&&h.$$applicationDestroyed();r(this,
-this.$$watchersCount);for(var b in this.$$listenerCount)s(this,this.$$listenerCount[b],b);a&&a.$$childHead===this&&(a.$$childHead=this.$$nextSibling);a&&a.$$childTail===this&&(a.$$childTail=this.$$prevSibling);this.$$prevSibling&&(this.$$prevSibling.$$nextSibling=this.$$nextSibling);this.$$nextSibling&&(this.$$nextSibling.$$prevSibling=this.$$prevSibling);this.$destroy=this.$digest=this.$apply=this.$evalAsync=this.$applyAsync=w;this.$on=this.$watch=this.$watchGroup=function(){return w};this.$$listeners=
{};this.$$nextSibling=null;l(this)}},$eval:function(a,b){return g(a)(this,b)},$evalAsync:function(a,b){K.$$phase||A.length||h.defer(function(){A.length&&K.$digest()});A.push({scope:this,expression:g(a),locals:b})},$$postDigest:function(a){v.push(a)},$apply:function(a){try{n("$apply");try{return this.$eval(a)}finally{K.$$phase=null}}catch(b){e(b)}finally{try{K.$digest()}catch(c){throw e(c),c;}}},$applyAsync:function(a){function b(){c.$eval(a)}var c=this;a&&t.push(b);a=g(a);p()},$on:function(a,b){var c=
this.$$listeners[a];c||(this.$$listeners[a]=c=[]);c.push(b);var d=this;do d.$$listenerCount[a]||(d.$$listenerCount[a]=0),d.$$listenerCount[a]++;while(d=d.$parent);var e=this;return function(){var d=c.indexOf(b);-1!==d&&(c[d]=null,s(e,1,a))}},$emit:function(a,b){var c=[],d,f=this,g=!1,h={name:a,targetScope:f,stopPropagation:function(){g=!0},preventDefault:function(){h.defaultPrevented=!0},defaultPrevented:!1},k=cb([h],arguments,1),l,m;do{d=f.$$listeners[a]||c;h.currentScope=f;l=0;for(m=d.length;l<
m;l++)if(d[l])try{d[l].apply(null,k)}catch(n){e(n)}else d.splice(l,1),l--,m--;if(g)return h.currentScope=null,h;f=f.$parent}while(f);h.currentScope=null;return h},$broadcast:function(a,b){var c=this,d=this,f={name:a,targetScope:this,preventDefault:function(){f.defaultPrevented=!0},defaultPrevented:!1};if(!this.$$listenerCount[a])return f;for(var g=cb([f],arguments,1),h,k;c=d;){f.currentScope=c;d=c.$$listeners[a]||[];h=0;for(k=d.length;h<k;h++)if(d[h])try{d[h].apply(null,g)}catch(l){e(l)}else d.splice(h,
1),h--,k--;if(!(d=c.$$listenerCount[a]&&c.$$childHead||c!==this&&c.$$nextSibling))for(;c!==this&&!(d=c.$$nextSibling);)c=c.$parent}f.currentScope=null;return f}};var K=new m,A=K.$$asyncQueue=[],v=K.$$postDigestQueue=[],t=K.$$applyAsyncQueue=[],L=0;return K}]}function Be(){var a=/^\s*(https?|ftp|mailto|tel|file):/,b=/^\s*((https?|ftp|file|blob):|data:image\/)/;this.aHrefSanitizationWhitelist=function(b){return x(b)?(a=b,this):a};this.imgSrcSanitizationWhitelist=function(a){return x(a)?(b=a,this):b};
this.$get=function(){return function(d,c){var f=c?b:a,e;e=ta(d).href;return""===e||e.match(f)?d:"unsafe:"+e}}}function Gg(a){if("self"===a)return a;if(D(a)){if(-1<a.indexOf("***"))throw Fa("iwcard",a);a=Jd(a).replace(/\\\*\\\*/g,".*").replace(/\\\*/g,"[^:/.?&;]*");return new RegExp("^"+a+"$")}if(Za(a))return new RegExp("^"+a.source+"$");throw Fa("imatcher");}function Kd(a){var b=[];x(a)&&q(a,function(a){b.push(Gg(a))});return b}function Mf(){this.SCE_CONTEXTS=ga;var a=["self"],b=[];this.resourceUrlWhitelist=
function(b){arguments.length&&(a=Kd(b));return a};this.resourceUrlBlacklist=function(a){arguments.length&&(b=Kd(a));return b};this.$get=["$injector",function(d){function c(a,b){return"self"===a?od(b):!!a.exec(b.href)}function f(a){var b=function(a){this.$$unwrapTrustedValue=function(){return a}};a&&(b.prototype=new a);b.prototype.valueOf=function(){return this.$$unwrapTrustedValue()};b.prototype.toString=function(){return this.$$unwrapTrustedValue().toString()};return b}var e=function(a){throw Fa("unsafe");
};d.has("$sanitize")&&(e=d.get("$sanitize"));var g=f(),h={};h[ga.HTML]=f(g);h[ga.CSS]=f(g);h[ga.URL]=f(g);h[ga.JS]=f(g);h[ga.RESOURCE_URL]=f(h[ga.URL]);return{trustAs:function(a,b){var c=h.hasOwnProperty(a)?h[a]:null;if(!c)throw Fa("icontext",a,b);if(null===b||z(b)||""===b)return b;if("string"!==typeof b)throw Fa("itype",a);return new c(b)},getTrusted:function(d,f){if(null===f||z(f)||""===f)return f;var g=h.hasOwnProperty(d)?h[d]:null;if(g&&f instanceof g)return f.$$unwrapTrustedValue();if(d===ga.RESOURCE_URL){var g=
ta(f.toString()),n,r,s=!1;n=0;for(r=a.length;n<r;n++)if(c(a[n],g)){s=!0;break}if(s)for(n=0,r=b.length;n<r;n++)if(c(b[n],g)){s=!1;break}if(s)return f;throw Fa("insecurl",f.toString());}if(d===ga.HTML)return e(f);throw Fa("unsafe");},valueOf:function(a){return a instanceof g?a.$$unwrapTrustedValue():a}}}]}function Lf(){var a=!0;this.enabled=function(b){arguments.length&&(a=!!b);return a};this.$get=["$parse","$sceDelegate",function(b,d){if(a&&8>Ia)throw Fa("iequirks");var c=ka(ga);c.isEnabled=function(){return a};
c.trustAs=d.trustAs;c.getTrusted=d.getTrusted;c.valueOf=d.valueOf;a||(c.trustAs=c.getTrusted=function(a,b){return b},c.valueOf=$a);c.parseAs=function(a,d){var e=b(d);return e.literal&&e.constant?e:b(d,function(b){return c.getTrusted(a,b)})};var f=c.parseAs,e=c.getTrusted,g=c.trustAs;q(ga,function(a,b){var d=Q(b);c[hb("parse_as_"+d)]=function(b){return f(a,b)};c[hb("get_trusted_"+d)]=function(b){return e(a,b)};c[hb("trust_as_"+d)]=function(b){return g(a,b)}});return c}]}function Nf(){this.$get=["$window",
"$document",function(a,b){var d={},c=!(a.chrome&&(a.chrome.app&&a.chrome.app.runtime||!a.chrome.app&&a.chrome.runtime&&a.chrome.runtime.id))&&a.history&&a.history.pushState,f=Z((/android (\d+)/.exec(Q((a.navigator||{}).userAgent))||[])[1]),e=/Boxee/i.test((a.navigator||{}).userAgent),g=b[0]||{},h,k=/^(Moz|webkit|ms)(?=[A-Z])/,l=g.body&&g.body.style,m=!1,n=!1;if(l){for(var r in l)if(m=k.exec(r)){h=m[0];h=h[0].toUpperCase()+h.substr(1);break}h||(h="WebkitOpacity"in l&&"webkit");m=!!("transition"in l||
h+"Transition"in l);n=!!("animation"in l||h+"Animation"in l);!f||m&&n||(m=D(l.webkitTransition),n=D(l.webkitAnimation))}return{history:!(!c||4>f||e),hasEvent:function(a){if("input"===a&&11>=Ia)return!1;if(z(d[a])){var b=g.createElement("div");d[a]="on"+a in b}return d[a]},csp:da(),vendorPrefix:h,transitions:m,animations:n,android:f}}]}function Pf(){var a;this.httpOptions=function(b){return b?(a=b,this):a};this.$get=["$templateCache","$http","$q","$sce",function(b,d,c,f){function e(g,h){e.totalPendingRequests++;
if(!D(g)||z(b.get(g)))g=f.getTrustedResourceUrl(g);var k=d.defaults&&d.defaults.transformResponse;I(k)?k=k.filter(function(a){return a!==gc}):k===gc&&(k=null);return d.get(g,R({cache:b,transformResponse:k},a))["finally"](function(){e.totalPendingRequests--}).then(function(a){b.put(g,a.data);return a.data},function(a){if(!h)throw Hg("tpload",g,a.status,a.statusText);return c.reject(a)})}e.totalPendingRequests=0;return e}]}function Qf(){this.$get=["$rootScope","$browser","$location",function(a,b,d){return{findBindings:function(a,
b,d){a=a.getElementsByClassName("ng-binding");var g=[];q(a,function(a){var c=$.element(a).data("$binding");c&&q(c,function(c){d?(new RegExp("(^|\\s)"+Jd(b)+"(\\s|\\||$)")).test(c)&&g.push(a):-1!==c.indexOf(b)&&g.push(a)})});return g},findModels:function(a,b,d){for(var g=["ng-","data-ng-","ng\\:"],h=0;h<g.length;++h){var k=a.querySelectorAll("["+g[h]+"model"+(d?"=":"*=")+'"'+b+'"]');if(k.length)return k}},getLocation:function(){return d.url()},setLocation:function(b){b!==d.url()&&(d.url(b),a.$digest())},
whenStable:function(a){b.notifyWhenNoOutstandingRequests(a)}}}]}function Rf(){this.$get=["$rootScope","$browser","$q","$$q","$exceptionHandler",function(a,b,d,c,f){function e(e,k,l){C(e)||(l=k,k=e,e=w);var m=va.call(arguments,3),n=x(l)&&!l,r=(n?c:d).defer(),s=r.promise,q;q=b.defer(function(){try{r.resolve(e.apply(null,m))}catch(b){r.reject(b),f(b)}finally{delete g[s.$$timeoutId]}n||a.$apply()},k);s.$$timeoutId=q;g[q]=r;return s}var g={};e.cancel=function(a){return a&&a.$$timeoutId in g?(g[a.$$timeoutId].reject("canceled"),
delete g[a.$$timeoutId],b.defer.cancel(a.$$timeoutId)):!1};return e}]}function ta(a){Ia&&(aa.setAttribute("href",a),a=aa.href);aa.setAttribute("href",a);return{href:aa.href,protocol:aa.protocol?aa.protocol.replace(/:$/,""):"",host:aa.host,search:aa.search?aa.search.replace(/^\?/,""):"",hash:aa.hash?aa.hash.replace(/^#/,""):"",hostname:aa.hostname,port:aa.port,pathname:"/"===aa.pathname.charAt(0)?aa.pathname:"/"+aa.pathname}}function od(a){a=D(a)?ta(a):a;return a.protocol===Ld.protocol&&a.host===Ld.host}
function Sf(){this.$get=ha(y)}function Md(a){function b(a){try{return decodeURIComponent(a)}catch(b){return a}}var d=a[0]||{},c={},f="";return function(){var a,g,h,k,l;try{a=d.cookie||""}catch(m){a=""}if(a!==f)for(f=a,a=f.split("; "),c={},h=0;h<a.length;h++)g=a[h],k=g.indexOf("="),0<k&&(l=b(g.substring(0,k)),z(c[l])&&(c[l]=b(g.substring(k+1))));return c}}function Wf(){this.$get=Md}function Rc(a){function b(d,c){if(E(d)){var f={};q(d,function(a,c){f[c]=b(c,a)});return f}return a.factory(d+"Filter",
c)}this.register=b;this.$get=["$injector",function(a){return function(b){return a.get(b+"Filter")}}];b("currency",Nd);b("date",Od);b("filter",Ig);b("json",Jg);b("limitTo",Kg);b("lowercase",Lg);b("number",Pd);b("orderBy",Qd);b("uppercase",Mg)}function Ig(){return function(a,b,d,c){if(!la(a)){if(null==a)return a;throw G("filter")("notarray",a);}c=c||"$";var f;switch(oc(b)){case "function":break;case "boolean":case "null":case "number":case "string":f=!0;case "object":b=Ng(b,d,c,f);break;default:return a}return Array.prototype.filter.call(a,
b)}}function Ng(a,b,d,c){var f=E(a)&&d in a;!0===b?b=na:C(b)||(b=function(a,b){if(z(a))return!1;if(null===a||null===b)return a===b;if(E(b)||E(a)&&!Ac(a))return!1;a=Q(""+a);b=Q(""+b);return-1!==a.indexOf(b)});return function(e){return f&&!E(e)?Na(e,a[d],b,d,!1):Na(e,a,b,d,c)}}function Na(a,b,d,c,f,e){var g=oc(a),h=oc(b);if("string"===h&&"!"===b.charAt(0))return!Na(a,b.substring(1),d,c,f);if(I(a))return a.some(function(a){return Na(a,b,d,c,f)});switch(g){case "object":var k;if(f){for(k in a)if("$"!==
k.charAt(0)&&Na(a[k],b,d,c,!0))return!0;return e?!1:Na(a,b,d,c,!1)}if("object"===h){for(k in b)if(e=b[k],!C(e)&&!z(e)&&(g=k===c,!Na(g?a:a[k],e,d,c,g,g)))return!1;return!0}return d(a,b);case "function":return!1;default:return d(a,b)}}function oc(a){return null===a?"null":typeof a}function Nd(a){var b=a.NUMBER_FORMATS;return function(a,c,f){z(c)&&(c=b.CURRENCY_SYM);z(f)&&(f=b.PATTERNS[1].maxFrac);return null==a?a:Rd(a,b.PATTERNS[1],b.GROUP_SEP,b.DECIMAL_SEP,f).replace(/\u00A4/g,c)}}function Pd(a){var b=
a.NUMBER_FORMATS;return function(a,c){return null==a?a:Rd(a,b.PATTERNS[0],b.GROUP_SEP,b.DECIMAL_SEP,c)}}function Og(a){var b=0,d,c,f,e,g;-1<(c=a.indexOf(Sd))&&(a=a.replace(Sd,""));0<(f=a.search(/e/i))?(0>c&&(c=f),c+=+a.slice(f+1),a=a.substring(0,f)):0>c&&(c=a.length);for(f=0;a.charAt(f)===pc;f++);if(f===(g=a.length))d=[0],c=1;else{for(g--;a.charAt(g)===pc;)g--;c-=f;d=[];for(e=0;f<=g;f++,e++)d[e]=+a.charAt(f)}c>Td&&(d=d.splice(0,Td-1),b=c-1,c=1);return{d:d,e:b,i:c}}function Pg(a,b,d,c){var f=a.d,e=
f.length-a.i;b=z(b)?Math.min(Math.max(d,e),c):+b;d=b+a.i;c=f[d];if(0<d){f.splice(Math.max(a.i,d));for(var g=d;g<f.length;g++)f[g]=0}else for(e=Math.max(0,e),a.i=1,f.length=Math.max(1,d=b+1),f[0]=0,g=1;g<d;g++)f[g]=0;if(5<=c)if(0>d-1){for(c=0;c>d;c--)f.unshift(0),a.i++;f.unshift(1);a.i++}else f[d-1]++;for(;e<Math.max(0,b);e++)f.push(0);if(b=f.reduceRight(function(a,b,c,d){b+=a;d[c]=b%10;return Math.floor(b/10)},0))f.unshift(b),a.i++}function Rd(a,b,d,c,f){if(!D(a)&&!ba(a)||isNaN(a))return"";var e=
!isFinite(a),g=!1,h=Math.abs(a)+"",k="";if(e)k="\u221e";else{g=Og(h);Pg(g,f,b.minFrac,b.maxFrac);k=g.d;h=g.i;f=g.e;e=[];for(g=k.reduce(function(a,b){return a&&!b},!0);0>h;)k.unshift(0),h++;0<h?e=k.splice(h,k.length):(e=k,k=[0]);h=[];for(k.length>=b.lgSize&&h.unshift(k.splice(-b.lgSize,k.length).join(""));k.length>b.gSize;)h.unshift(k.splice(-b.gSize,k.length).join(""));k.length&&h.unshift(k.join(""));k=h.join(d);e.length&&(k+=c+e.join(""));f&&(k+="e+"+f)}return 0>a&&!g?b.negPre+k+b.negSuf:b.posPre+
k+b.posSuf}function Mb(a,b,d,c){var f="";if(0>a||c&&0>=a)c?a=-a+1:(a=-a,f="-");for(a=""+a;a.length<b;)a=pc+a;d&&(a=a.substr(a.length-b));return f+a}function U(a,b,d,c,f){d=d||0;return function(e){e=e["get"+a]();if(0<d||e>-d)e+=d;0===e&&-12===d&&(e=12);return Mb(e,b,c,f)}}function nb(a,b,d){return function(c,f){var e=c["get"+a](),g=wb((d?"STANDALONE":"")+(b?"SHORT":"")+a);return f[g][e]}}function Ud(a){var b=(new Date(a,0,1)).getDay();return new Date(a,0,(4>=b?5:12)-b)}function Vd(a){return function(b){var d=
Ud(b.getFullYear());b=+new Date(b.getFullYear(),b.getMonth(),b.getDate()+(4-b.getDay()))-+d;b=1+Math.round(b/6048E5);return Mb(b,a)}}function qc(a,b){return 0>=a.getFullYear()?b.ERAS[0]:b.ERAS[1]}function Od(a){function b(a){var b;if(b=a.match(d)){a=new Date(0);var e=0,g=0,h=b[8]?a.setUTCFullYear:a.setFullYear,k=b[8]?a.setUTCHours:a.setHours;b[9]&&(e=Z(b[9]+b[10]),g=Z(b[9]+b[11]));h.call(a,Z(b[1]),Z(b[2])-1,Z(b[3]));e=Z(b[4]||0)-e;g=Z(b[5]||0)-g;h=Z(b[6]||0);b=Math.round(1E3*parseFloat("0."+(b[7]||
0)));k.call(a,e,g,h,b)}return a}var d=/^(\d{4})-?(\d\d)-?(\d\d)(?:T(\d\d)(?::?(\d\d)(?::?(\d\d)(?:\.(\d+))?)?)?(Z|([+-])(\d\d):?(\d\d))?)?$/;return function(c,d,e){var g="",h=[],k,l;d=d||"mediumDate";d=a.DATETIME_FORMATS[d]||d;D(c)&&(c=Qg.test(c)?Z(c):b(c));ba(c)&&(c=new Date(c));if(!ja(c)||!isFinite(c.getTime()))return c;for(;d;)(l=Rg.exec(d))?(h=cb(h,l,1),d=h.pop()):(h.push(d),d=null);var m=c.getTimezoneOffset();e&&(m=Dc(e,m),c=Ub(c,e,!0));q(h,function(b){k=Sg[b];g+=k?k(c,a.DATETIME_FORMATS,m):
"''"===b?"'":b.replace(/(^'|'$)/g,"").replace(/''/g,"'")});return g}}function Jg(){return function(a,b){z(b)&&(b=2);return eb(a,b)}}function Kg(){return function(a,b,d){b=Infinity===Math.abs(Number(b))?Number(b):Z(b);if(ia(b))return a;ba(a)&&(a=a.toString());if(!la(a))return a;d=!d||isNaN(d)?0:Z(d);d=0>d?Math.max(0,a.length+d):d;return 0<=b?rc(a,d,d+b):0===d?rc(a,b,a.length):rc(a,Math.max(0,d+b),d)}}function rc(a,b,d){return D(a)?a.slice(b,d):va.call(a,b,d)}function Qd(a){function b(b){return b.map(function(b){var c=
1,d=$a;if(C(b))d=b;else if(D(b)){if("+"===b.charAt(0)||"-"===b.charAt(0))c="-"===b.charAt(0)?-1:1,b=b.substring(1);if(""!==b&&(d=a(b),d.constant))var f=d(),d=function(a){return a[f]}}return{get:d,descending:c}})}function d(a){switch(typeof a){case "number":case "boolean":case "string":return!0;default:return!1}}function c(a,b){var c=0,d=a.type,k=b.type;if(d===k){var k=a.value,l=b.value;"string"===d?(k=k.toLowerCase(),l=l.toLowerCase()):"object"===d&&(E(k)&&(k=a.index),E(l)&&(l=b.index));k!==l&&(c=
k<l?-1:1)}else c=d<k?-1:1;return c}return function(a,e,g,h){if(null==a)return a;if(!la(a))throw G("orderBy")("notarray",a);I(e)||(e=[e]);0===e.length&&(e=["+"]);var k=b(e),l=g?-1:1,m=C(h)?h:c;a=Array.prototype.map.call(a,function(a,b){return{value:a,tieBreaker:{value:b,type:"number",index:b},predicateValues:k.map(function(c){var e=c.get(a);c=typeof e;if(null===e)c="string",e="null";else if("object"===c)a:{if(C(e.valueOf)&&(e=e.valueOf(),d(e)))break a;Ac(e)&&(e=e.toString(),d(e))}return{value:e,type:c,
index:b}})}});a.sort(function(a,b){for(var c=0,d=k.length;c<d;c++){var e=m(a.predicateValues[c],b.predicateValues[c]);if(e)return e*k[c].descending*l}return m(a.tieBreaker,b.tieBreaker)*l});return a=a.map(function(a){return a.value})}}function Va(a){C(a)&&(a={link:a});a.restrict=a.restrict||"AC";return ha(a)}function Wd(a,b,d,c,f){var e=this,g=[];e.$error={};e.$$success={};e.$pending=void 0;e.$name=f(b.name||b.ngForm||"")(d);e.$dirty=!1;e.$pristine=!0;e.$valid=!0;e.$invalid=!1;e.$submitted=!1;e.$$parentForm=
Nb;e.$rollbackViewValue=function(){q(g,function(a){a.$rollbackViewValue()})};e.$commitViewValue=function(){q(g,function(a){a.$commitViewValue()})};e.$addControl=function(a){Ra(a.$name,"input");g.push(a);a.$name&&(e[a.$name]=a);a.$$parentForm=e};e.$$renameControl=function(a,b){var c=a.$name;e[c]===a&&delete e[c];e[b]=a;a.$name=b};e.$removeControl=function(a){a.$name&&e[a.$name]===a&&delete e[a.$name];q(e.$pending,function(b,c){e.$setValidity(c,null,a)});q(e.$error,function(b,c){e.$setValidity(c,null,
a)});q(e.$$success,function(b,c){e.$setValidity(c,null,a)});bb(g,a);a.$$parentForm=Nb};Xd({ctrl:this,$element:a,set:function(a,b,c){var d=a[b];d?-1===d.indexOf(c)&&d.push(c):a[b]=[c]},unset:function(a,b,c){var d=a[b];d&&(bb(d,c),0===d.length&&delete a[b])},$animate:c});e.$setDirty=function(){c.removeClass(a,Wa);c.addClass(a,Ob);e.$dirty=!0;e.$pristine=!1;e.$$parentForm.$setDirty()};e.$setPristine=function(){c.setClass(a,Wa,Ob+" ng-submitted");e.$dirty=!1;e.$pristine=!0;e.$submitted=!1;q(g,function(a){a.$setPristine()})};
e.$setUntouched=function(){q(g,function(a){a.$setUntouched()})};e.$setSubmitted=function(){c.addClass(a,"ng-submitted");e.$submitted=!0;e.$$parentForm.$setSubmitted()}}function sc(a){a.$formatters.push(function(b){return a.$isEmpty(b)?b:b.toString()})}function Xa(a,b,d,c,f,e){var g=Q(b[0].type);if(!f.android){var h=!1;b.on("compositionstart",function(){h=!0});b.on("compositionend",function(){h=!1;l()})}var k,l=function(a){k&&(e.defer.cancel(k),k=null);if(!h){var f=b.val();a=a&&a.type;"password"===
g||d.ngTrim&&"false"===d.ngTrim||(f=Y(f));(c.$viewValue!==f||""===f&&c.$$hasNativeValidators)&&c.$setViewValue(f,a)}};if(f.hasEvent("input"))b.on("input",l);else{var m=function(a,b,c){k||(k=e.defer(function(){k=null;b&&b.value===c||l(a)}))};b.on("keydown",function(a){var b=a.keyCode;91===b||15<b&&19>b||37<=b&&40>=b||m(a,this,this.value)});if(f.hasEvent("paste"))b.on("paste cut",m)}b.on("change",l);if(Yd[g]&&c.$$hasNativeValidators&&g===d.type)b.on("keydown wheel mousedown",function(a){if(!k){var b=
this.validity,c=b.badInput,d=b.typeMismatch;k=e.defer(function(){k=null;b.badInput===c&&b.typeMismatch===d||l(a)})}});c.$render=function(){var a=c.$isEmpty(c.$viewValue)?"":c.$viewValue;b.val()!==a&&b.val(a)}}function Pb(a,b){return function(d,c){var f,e;if(ja(d))return d;if(D(d)){'"'===d.charAt(0)&&'"'===d.charAt(d.length-1)&&(d=d.substring(1,d.length-1));if(Tg.test(d))return new Date(d);a.lastIndex=0;if(f=a.exec(d))return f.shift(),e=c?{yyyy:c.getFullYear(),MM:c.getMonth()+1,dd:c.getDate(),HH:c.getHours(),
mm:c.getMinutes(),ss:c.getSeconds(),sss:c.getMilliseconds()/1E3}:{yyyy:1970,MM:1,dd:1,HH:0,mm:0,ss:0,sss:0},q(f,function(a,c){c<b.length&&(e[b[c]]=+a)}),new Date(e.yyyy,e.MM-1,e.dd,e.HH,e.mm,e.ss||0,1E3*e.sss||0)}return NaN}}function ob(a,b,d,c){return function(f,e,g,h,k,l,m){function n(a){return a&&!(a.getTime&&a.getTime()!==a.getTime())}function r(a){return x(a)&&!ja(a)?d(a)||void 0:a}tc(f,e,g,h);Xa(f,e,g,h,k,l);var s=h&&h.$options&&h.$options.timezone,q;h.$$parserName=a;h.$parsers.push(function(a){if(h.$isEmpty(a))return null;
if(b.test(a))return a=d(a,q),s&&(a=Ub(a,s)),a});h.$formatters.push(function(a){if(a&&!ja(a))throw pb("datefmt",a);if(n(a))return(q=a)&&s&&(q=Ub(q,s,!0)),m("date")(a,c,s);q=null;return""});if(x(g.min)||g.ngMin){var u;h.$validators.min=function(a){return!n(a)||z(u)||d(a)>=u};g.$observe("min",function(a){u=r(a);h.$validate()})}if(x(g.max)||g.ngMax){var p;h.$validators.max=function(a){return!n(a)||z(p)||d(a)<=p};g.$observe("max",function(a){p=r(a);h.$validate()})}}}function tc(a,b,d,c){(c.$$hasNativeValidators=
E(b[0].validity))&&c.$parsers.push(function(a){var c=b.prop("validity")||{};return c.badInput||c.typeMismatch?void 0:a})}function Zd(a){a.$$parserName="number";a.$parsers.push(function(b){if(a.$isEmpty(b))return null;if(Ug.test(b))return parseFloat(b)});a.$formatters.push(function(b){if(!a.$isEmpty(b)){if(!ba(b))throw pb("numfmt",b);b=b.toString()}return b})}function qb(a){x(a)&&!ba(a)&&(a=parseFloat(a));return ia(a)?void 0:a}function uc(a){var b=a.toString(),d=b.indexOf(".");return-1===d?-1<a&&1>
a&&(a=/e-(\d+)$/.exec(b))?Number(a[1]):0:b.length-d-1}function $d(a,b,d,c,f){if(x(c)){a=a(c);if(!a.constant)throw pb("constexpr",d,c);return a(b)}return f}function vc(a,b){a="ngClass"+a;return["$animate",function(d){function c(a,b){var c=[],d=0;a:for(;d<a.length;d++){for(var f=a[d],m=0;m<b.length;m++)if(f===b[m])continue a;c.push(f)}return c}function f(a){var b=[];return I(a)?(q(a,function(a){b=b.concat(f(a))}),b):D(a)?a.split(" "):E(a)?(q(a,function(a,c){a&&(b=b.concat(c.split(" ")))}),b):a}return{restrict:"AC",
link:function(e,g,h){function k(a){a=l(a,1);h.$addClass(a)}function l(a,b){var c=g.data("$classCounts")||V(),d=[];q(a,function(a){if(0<b||c[a])c[a]=(c[a]||0)+b,c[a]===+(0<b)&&d.push(a)});g.data("$classCounts",c);return d.join(" ")}function m(a,b){var e=c(b,a),f=c(a,b),e=l(e,1),f=l(f,-1);e&&e.length&&d.addClass(g,e);f&&f.length&&d.removeClass(g,f)}function n(a){if(!0===b||(e.$index&1)===b){var c=f(a||[]);if(!r)k(c);else if(!na(a,r)){var d=f(r);m(d,c)}}r=I(a)?a.map(function(a){return ka(a)}):ka(a)}
var r;h.$observe("class",function(b){n(e.$eval(h[a]))});"ngClass"!==a&&e.$watch("$index",function(a,c){var d=a&1;if(d!==(c&1)){var e=f(r);d===b?k(e):(d=l(e,-1),h.$removeClass(d))}});e.$watch(h[a],n,!0)}}}]}function Xd(a){function b(a,b){b&&!e[a]?(k.addClass(f,a),e[a]=!0):!b&&e[a]&&(k.removeClass(f,a),e[a]=!1)}function d(a,c){a=a?"-"+Hc(a,"-"):"";b(rb+a,!0===c);b(ae+a,!1===c)}var c=a.ctrl,f=a.$element,e={},g=a.set,h=a.unset,k=a.$animate;e[ae]=!(e[rb]=f.hasClass(rb));c.$setValidity=function(a,e,f){z(e)?
(c.$pending||(c.$pending={}),g(c.$pending,a,f)):(c.$pending&&h(c.$pending,a,f),be(c.$pending)&&(c.$pending=void 0));Ka(e)?e?(h(c.$error,a,f),g(c.$$success,a,f)):(g(c.$error,a,f),h(c.$$success,a,f)):(h(c.$error,a,f),h(c.$$success,a,f));c.$pending?(b(ce,!0),c.$valid=c.$invalid=void 0,d("",null)):(b(ce,!1),c.$valid=be(c.$error),c.$invalid=!c.$valid,d("",c.$valid));e=c.$pending&&c.$pending[a]?void 0:c.$error[a]?!1:c.$$success[a]?!0:null;d(a,e);c.$$parentForm.$setValidity(a,e,c)}}function be(a){if(a)for(var b in a)if(a.hasOwnProperty(b))return!1;
return!0}var Vg=/^\/(.+)\/([a-z]*)$/,ua=Object.prototype.hasOwnProperty,Q=function(a){return D(a)?a.toLowerCase():a},wb=function(a){return D(a)?a.toUpperCase():a},Ia,F,za,va=[].slice,pg=[].splice,Wg=[].push,ma=Object.prototype.toString,Bc=Object.getPrototypeOf,xa=G("ng"),$=y.angular||(y.angular={}),Wb,sb=0;Ia=y.document.documentMode;var ia=Number.isNaN||function(a){return a!==a};w.$inject=[];$a.$inject=[];var I=Array.isArray,ne=/^\[object (?:Uint8|Uint8Clamped|Uint16|Uint32|Int8|Int16|Int32|Float32|Float64)Array]$/,
Y=function(a){return D(a)?a.trim():a},Jd=function(a){return a.replace(/([-()[\]{}+?*.$^|,:#<!\\])/g,"\\$1").replace(/\x08/g,"\\x08")},da=function(){if(!x(da.rules)){var a=y.document.querySelector("[ng-csp]")||y.document.querySelector("[data-ng-csp]");if(a){var b=a.getAttribute("ng-csp")||a.getAttribute("data-ng-csp");da.rules={noUnsafeEval:!b||-1!==b.indexOf("no-unsafe-eval"),noInlineStyle:!b||-1!==b.indexOf("no-inline-style")}}else{a=da;try{new Function(""),b=!1}catch(d){b=!0}a.rules={noUnsafeEval:b,
noInlineStyle:!1}}}return da.rules},ub=function(){if(x(ub.name_))return ub.name_;var a,b,d=Oa.length,c,f;for(b=0;b<d;++b)if(c=Oa[b],a=y.document.querySelector("["+c.replace(":","\\:")+"jq]")){f=a.getAttribute(c+"jq");break}return ub.name_=f},qe=/:/g,Oa=["ng-","data-ng-","ng:","x-ng-"],te=function(a){var b=a.currentScript,b=b&&b.getAttribute("src");if(!b)return!0;var d=a.createElement("a");d.href=b;if(a.location.origin===d.origin)return!0;switch(d.protocol){case "http:":case "https:":case "ftp:":case "blob:":case "file:":case "data:":return!0;
default:return!1}}(y.document),we=/[A-Z]/g,Ic=!1,La=3,Ae={full:"1.5.11",major:1,minor:5,dot:11,codeName:"princely-quest"};W.expando="ng339";var jb=W.cache={},bg=1;W._data=function(a){return this.cache[a[this.expando]]||{}};var Xf=/([:\-_]+(.))/g,Yf=/^moz([A-Z])/,Ab={mouseleave:"mouseout",mouseenter:"mouseover"},Yb=G("jqLite"),ag=/^<([\w-]+)\s*\/?>(?:<\/\1>|)$/,Xb=/<|&#?\w+;/,Zf=/<([\w:-]+)/,$f=/<(?!area|br|col|embed|hr|img|input|link|meta|param)(([\w:-]+)[^>]*)\/>/gi,pa={option:[1,'<select multiple="multiple">',
"</select>"],thead:[1,"<table>","</table>"],col:[2,"<table><colgroup>","</colgroup></table>"],tr:[2,"<table><tbody>","</tbody></table>"],td:[3,"<table><tbody><tr>","</tr></tbody></table>"],_default:[0,"",""]};pa.optgroup=pa.option;pa.tbody=pa.tfoot=pa.colgroup=pa.caption=pa.thead;pa.th=pa.td;var gg=y.Node.prototype.contains||function(a){return!!(this.compareDocumentPosition(a)&16)},Pa=W.prototype={ready:function(a){function b(){d||(d=!0,a())}var d=!1;"complete"===y.document.readyState?y.setTimeout(b):
(this.on("DOMContentLoaded",b),W(y).on("load",b))},toString:function(){var a=[];q(this,function(b){a.push(""+b)});return"["+a.join(", ")+"]"},eq:function(a){return 0<=a?F(this[a]):F(this[this.length+a])},length:0,push:Wg,sort:[].sort,splice:[].splice},Gb={};q("multiple selected checked disabled readOnly required open".split(" "),function(a){Gb[Q(a)]=a});var $c={};q("input select option textarea button form details".split(" "),function(a){$c[a]=!0});var gd={ngMinlength:"minlength",ngMaxlength:"maxlength",
ngMin:"min",ngMax:"max",ngPattern:"pattern"};q({data:$b,removeData:ib,hasData:function(a){for(var b in jb[a.ng339])return!0;return!1},cleanData:function(a){for(var b=0,d=a.length;b<d;b++)ib(a[b])}},function(a,b){W[b]=a});q({data:$b,inheritedData:Eb,scope:function(a){return F.data(a,"$scope")||Eb(a.parentNode||a,["$isolateScope","$scope"])},isolateScope:function(a){return F.data(a,"$isolateScope")||F.data(a,"$isolateScopeNoTemplate")},controller:Xc,injector:function(a){return Eb(a,"$injector")},removeAttr:function(a,
b){a.removeAttribute(b)},hasClass:Bb,css:function(a,b,d){b=hb(b);if(x(d))a.style[b]=d;else return a.style[b]},attr:function(a,b,d){var c=a.nodeType;if(c!==La&&2!==c&&8!==c)if(c=Q(b),Gb[c])if(x(d))d?(a[b]=!0,a.setAttribute(b,c)):(a[b]=!1,a.removeAttribute(c));else return a[b]||(a.attributes.getNamedItem(b)||w).specified?c:void 0;else if(x(d))a.setAttribute(b,d);else if(a.getAttribute)return a=a.getAttribute(b,2),null===a?void 0:a},prop:function(a,b,d){if(x(d))a[b]=d;else return a[b]},text:function(){function a(a,
d){if(z(d)){var c=a.nodeType;return 1===c||c===La?a.textContent:""}a.textContent=d}a.$dv="";return a}(),val:function(a,b){if(z(b)){if(a.multiple&&"select"===wa(a)){var d=[];q(a.options,function(a){a.selected&&d.push(a.value||a.text)});return 0===d.length?null:d}return a.value}a.value=b},html:function(a,b){if(z(b))return a.innerHTML;yb(a,!0);a.innerHTML=b},empty:Yc},function(a,b){W.prototype[b]=function(b,c){var f,e,g=this.length;if(a!==Yc&&z(2===a.length&&a!==Bb&&a!==Xc?b:c)){if(E(b)){for(f=0;f<g;f++)if(a===
$b)a(this[f],b);else for(e in b)a(this[f],e,b[e]);return this}f=a.$dv;g=z(f)?Math.min(g,1):g;for(e=0;e<g;e++){var h=a(this[e],b,c);f=f?f+h:h}return f}for(f=0;f<g;f++)a(this[f],b,c);return this}});q({removeData:ib,on:function(a,b,d,c){if(x(c))throw Yb("onargs");if(Sc(a)){c=zb(a,!0);var f=c.events,e=c.handle;e||(e=c.handle=dg(a,f));c=0<=b.indexOf(" ")?b.split(" "):[b];for(var g=c.length,h=function(b,c,g){var h=f[b];h||(h=f[b]=[],h.specialHandlerWrapper=c,"$destroy"===b||g||a.addEventListener(b,e,!1));
h.push(d)};g--;)b=c[g],Ab[b]?(h(Ab[b],fg),h(b,void 0,!0)):h(b)}},off:Wc,one:function(a,b,d){a=F(a);a.on(b,function f(){a.off(b,d);a.off(b,f)});a.on(b,d)},replaceWith:function(a,b){var d,c=a.parentNode;yb(a);q(new W(b),function(b){d?c.insertBefore(b,d.nextSibling):c.replaceChild(b,a);d=b})},children:function(a){var b=[];q(a.childNodes,function(a){1===a.nodeType&&b.push(a)});return b},contents:function(a){return a.contentDocument||a.childNodes||[]},append:function(a,b){var d=a.nodeType;if(1===d||11===
d){b=new W(b);for(var d=0,c=b.length;d<c;d++)a.appendChild(b[d])}},prepend:function(a,b){if(1===a.nodeType){var d=a.firstChild;q(new W(b),function(b){a.insertBefore(b,d)})}},wrap:function(a,b){Uc(a,F(b).eq(0).clone()[0])},remove:Fb,detach:function(a){Fb(a,!0)},after:function(a,b){var d=a,c=a.parentNode;if(c){b=new W(b);for(var f=0,e=b.length;f<e;f++){var g=b[f];c.insertBefore(g,d.nextSibling);d=g}}},addClass:Db,removeClass:Cb,toggleClass:function(a,b,d){b&&q(b.split(" "),function(b){var f=d;z(f)&&
(f=!Bb(a,b));(f?Db:Cb)(a,b)})},parent:function(a){return(a=a.parentNode)&&11!==a.nodeType?a:null},next:function(a){return a.nextElementSibling},find:function(a,b){return a.getElementsByTagName?a.getElementsByTagName(b):[]},clone:Zb,triggerHandler:function(a,b,d){var c,f,e=b.type||b,g=zb(a);if(g=(g=g&&g.events)&&g[e])c={preventDefault:function(){this.defaultPrevented=!0},isDefaultPrevented:function(){return!0===this.defaultPrevented},stopImmediatePropagation:function(){this.immediatePropagationStopped=
!0},isImmediatePropagationStopped:function(){return!0===this.immediatePropagationStopped},stopPropagation:w,type:e,target:a},b.type&&(c=R(c,b)),b=ka(g),f=d?[c].concat(d):[c],q(b,function(b){c.isImmediatePropagationStopped()||b.apply(a,f)})}},function(a,b){W.prototype[b]=function(b,c,f){for(var e,g=0,h=this.length;g<h;g++)z(e)?(e=a(this[g],b,c,f),x(e)&&(e=F(e))):Vc(e,a(this[g],b,c,f));return x(e)?e:this}});W.prototype.bind=W.prototype.on;W.prototype.unbind=W.prototype.off;Sa.prototype={put:function(a,
b){this[Aa(a,this.nextUid)]=b},get:function(a){return this[Aa(a,this.nextUid)]},remove:function(a){var b=this[a=Aa(a,this.nextUid)];delete this[a];return b}};var Vf=[function(){this.$get=[function(){return Sa}]}],ig=/^([^(]+?)=>/,jg=/^[^(]*\(\s*([^)]*)\)/m,Xg=/,/,Yg=/^\s*(_?)(\S+?)\1\s*$/,hg=/((\/\/.*$)|(\/\*[\s\S]*?\*\/))/mg,Ba=G("$injector");fb.$$annotate=function(a,b,d){var c;if("function"===typeof a){if(!(c=a.$inject)){c=[];if(a.length){if(b)throw D(d)&&d||(d=a.name||kg(a)),Ba("strictdi",d);b=
ad(a);q(b[1].split(Xg),function(a){a.replace(Yg,function(a,b,d){c.push(d)})})}a.$inject=c}}else I(a)?(b=a.length-1,Qa(a[b],"fn"),c=a.slice(0,b)):Qa(a,"fn",!0);return c};var de=G("$animate"),nf=function(){this.$get=w},of=function(){var a=new Sa,b=[];this.$get=["$$AnimateRunner","$rootScope",function(d,c){function f(a,b,c){var d=!1;b&&(b=D(b)?b.split(" "):I(b)?b:[],q(b,function(b){b&&(d=!0,a[b]=c)}));return d}function e(){q(b,function(b){var c=a.get(b);if(c){var d=lg(b.attr("class")),e="",f="";q(c,
function(a,b){a!==!!d[b]&&(a?e+=(e.length?" ":"")+b:f+=(f.length?" ":"")+b)});q(b,function(a){e&&Db(a,e);f&&Cb(a,f)});a.remove(b)}});b.length=0}return{enabled:w,on:w,off:w,pin:w,push:function(g,h,k,l){l&&l();k=k||{};k.from&&g.css(k.from);k.to&&g.css(k.to);if(k.addClass||k.removeClass)if(h=k.addClass,l=k.removeClass,k=a.get(g)||{},h=f(k,h,!0),l=f(k,l,!1),h||l)a.put(g,k),b.push(g),1===b.length&&c.$$postDigest(e);g=new d;g.complete();return g}}}]},lf=["$provide",function(a){var b=this;this.$$registeredAnimations=
Object.create(null);this.register=function(d,c){if(d&&"."!==d.charAt(0))throw de("notcsel",d);var f=d+"-animation";b.$$registeredAnimations[d.substr(1)]=f;a.factory(f,c)};this.classNameFilter=function(a){if(1===arguments.length&&(this.$$classNameFilter=a instanceof RegExp?a:null)&&/(\s+|\/)ng-animate(\s+|\/)/.test(this.$$classNameFilter.toString()))throw de("nongcls","ng-animate");return this.$$classNameFilter};this.$get=["$$animateQueue",function(a){function b(a,c,d){if(d){var h;a:{for(h=0;h<d.length;h++){var k=
d[h];if(1===k.nodeType){h=k;break a}}h=void 0}!h||h.parentNode||h.previousElementSibling||(d=null)}d?d.after(a):c.prepend(a)}return{on:a.on,off:a.off,pin:a.pin,enabled:a.enabled,cancel:function(a){a.end&&a.end()},enter:function(f,e,g,h){e=e&&F(e);g=g&&F(g);e=e||g.parent();b(f,e,g);return a.push(f,"enter",Ca(h))},move:function(f,e,g,h){e=e&&F(e);g=g&&F(g);e=e||g.parent();b(f,e,g);return a.push(f,"move",Ca(h))},leave:function(b,c){return a.push(b,"leave",Ca(c),function(){b.remove()})},addClass:function(b,
c,g){g=Ca(g);g.addClass=kb(g.addclass,c);return a.push(b,"addClass",g)},removeClass:function(b,c,g){g=Ca(g);g.removeClass=kb(g.removeClass,c);return a.push(b,"removeClass",g)},setClass:function(b,c,g,h){h=Ca(h);h.addClass=kb(h.addClass,c);h.removeClass=kb(h.removeClass,g);return a.push(b,"setClass",h)},animate:function(b,c,g,h,k){k=Ca(k);k.from=k.from?R(k.from,c):c;k.to=k.to?R(k.to,g):g;k.tempClasses=kb(k.tempClasses,h||"ng-inline-animate");return a.push(b,"animate",k)}}}]}],qf=function(){this.$get=
["$$rAF",function(a){function b(b){d.push(b);1<d.length||a(function(){for(var a=0;a<d.length;a++)d[a]();d=[]})}var d=[];return function(){var a=!1;b(function(){a=!0});return function(d){a?d():b(d)}}}]},pf=function(){this.$get=["$q","$sniffer","$$animateAsyncRun","$document","$timeout",function(a,b,d,c,f){function e(a){this.setHost(a);var b=d();this._doneCallbacks=[];this._tick=function(a){var d=c[0];d&&d.hidden?f(a,0,!1):b(a)};this._state=0}e.chain=function(a,b){function c(){if(d===a.length)b(!0);
else a[d](function(a){!1===a?b(!1):(d++,c())})}var d=0;c()};e.all=function(a,b){function c(f){e=e&&f;++d===a.length&&b(e)}var d=0,e=!0;q(a,function(a){a.done(c)})};e.prototype={setHost:function(a){this.host=a||{}},done:function(a){2===this._state?a():this._doneCallbacks.push(a)},progress:w,getPromise:function(){if(!this.promise){var b=this;this.promise=a(function(a,c){b.done(function(b){!1===b?c():a()})})}return this.promise},then:function(a,b){return this.getPromise().then(a,b)},"catch":function(a){return this.getPromise()["catch"](a)},
"finally":function(a){return this.getPromise()["finally"](a)},pause:function(){this.host.pause&&this.host.pause()},resume:function(){this.host.resume&&this.host.resume()},end:function(){this.host.end&&this.host.end();this._resolve(!0)},cancel:function(){this.host.cancel&&this.host.cancel();this._resolve(!1)},complete:function(a){var b=this;0===b._state&&(b._state=1,b._tick(function(){b._resolve(a)}))},_resolve:function(a){2!==this._state&&(q(this._doneCallbacks,function(b){b(a)}),this._doneCallbacks.length=
0,this._state=2)}};return e}]},mf=function(){this.$get=["$$rAF","$q","$$AnimateRunner",function(a,b,d){return function(b,f){function e(){a(function(){g.addClass&&(b.addClass(g.addClass),g.addClass=null);g.removeClass&&(b.removeClass(g.removeClass),g.removeClass=null);g.to&&(b.css(g.to),g.to=null);h||k.complete();h=!0});return k}var g=f||{};g.$$prepared||(g=sa(g));g.cleanupStyles&&(g.from=g.to=null);g.from&&(b.css(g.from),g.from=null);var h,k=new d;return{start:e,end:e}}}]},fa=G("$compile"),ec=new function(){};
Kc.$inject=["$provide","$$sanitizeUriProvider"];Hb.prototype.isFirstChange=function(){return this.previousValue===ec};var bd=/^((?:x|data)[:\-_])/i,id=G("$controller"),hd=/^(\S+)(\s+as\s+([\w$]+))?$/,wf=function(){this.$get=["$document",function(a){return function(b){b?!b.nodeType&&b instanceof F&&(b=b[0]):b=a[0].body;return b.offsetWidth+1}}]},jd="application/json",hc={"Content-Type":jd+";charset=utf-8"},rg=/^\[|^\{(?!\{)/,sg={"[":/]$/,"{":/}$/},qg=/^\)]\}',?\n/,Zg=G("$http"),nd=function(a){return function(){throw Zg("legacy",
a);}},Ha=$.$interpolateMinErr=G("$interpolate");Ha.throwNoconcat=function(a){throw Ha("noconcat",a);};Ha.interr=function(a,b){return Ha("interr",a,b.toString())};var Ef=function(){this.$get=["$window",function(a){function b(a){var b=function(a){b.data=a;b.called=!0};b.id=a;return b}var d=a.angular.callbacks,c={};return{createCallback:function(a){a="_"+(d.$$counter++).toString(36);var e="angular.callbacks."+a,g=b(a);c[e]=d[a]=g;return e},wasCalled:function(a){return c[a].called},getResponse:function(a){return c[a].data},
removeCallback:function(a){delete d[c[a].id];delete c[a]}}}]},$g=/^([^?#]*)(\?([^#]*))?(#(.*))?$/,ug={http:80,https:443,ftp:21},lb=G("$location"),vg=/^\s*[\\/]{2,}/,ah={$$absUrl:"",$$html5:!1,$$replace:!1,absUrl:Ib("$$absUrl"),url:function(a){if(z(a))return this.$$url;var b=$g.exec(a);(b[1]||""===a)&&this.path(decodeURIComponent(b[1]));(b[2]||b[1]||""===a)&&this.search(b[3]||"");this.hash(b[5]||"");return this},protocol:Ib("$$protocol"),host:Ib("$$host"),port:Ib("$$port"),path:sd("$$path",function(a){a=
null!==a?a.toString():"";return"/"===a.charAt(0)?a:"/"+a}),search:function(a,b){switch(arguments.length){case 0:return this.$$search;case 1:if(D(a)||ba(a))a=a.toString(),this.$$search=Fc(a);else if(E(a))a=sa(a,{}),q(a,function(b,c){null==b&&delete a[c]}),this.$$search=a;else throw lb("isrcharg");break;default:z(b)||null===b?delete this.$$search[a]:this.$$search[a]=b}this.$$compose();return this},hash:sd("$$hash",function(a){return null!==a?a.toString():""}),replace:function(){this.$$replace=!0;return this}};
q([rd,kc,jc],function(a){a.prototype=Object.create(ah);a.prototype.state=function(b){if(!arguments.length)return this.$$state;if(a!==jc||!this.$$html5)throw lb("nostate");this.$$state=z(b)?null:b;return this}});var ea=G("$parse"),ud=[].constructor,vd=(!1).constructor,wd=Function.constructor,xd=(0).constructor,yd={}.constructor,zd="".constructor,Ag=ud.prototype,Bg=vd.prototype,Kb=wd.prototype,Cg=xd.prototype,Ad=yd.prototype,Dg=zd.prototype,xg=Kb.call,yg=Kb.apply,zg=Kb.bind,Fg=Ad.valueOf,Qb=V();q("+ - * / % === !== == != < > <= >= && || ! = |".split(" "),
function(a){Qb[a]=!0});var bh={n:"\n",f:"\f",r:"\r",t:"\t",v:"\v","'":"'",'"':'"'},mc=function(a){this.options=a};mc.prototype={constructor:mc,lex:function(a){this.text=a;this.index=0;for(this.tokens=[];this.index<this.text.length;)if(a=this.text.charAt(this.index),'"'===a||"'"===a)this.readString(a);else if(this.isNumber(a)||"."===a&&this.isNumber(this.peek()))this.readNumber();else if(this.isIdentifierStart(this.peekMultichar()))this.readIdent();else if(this.is(a,"(){}[].,;:?"))this.tokens.push({index:this.index,
text:a}),this.index++;else if(this.isWhitespace(a))this.index++;else{var b=a+this.peek(),d=b+this.peek(2),c=Qb[b],f=Qb[d];Qb[a]||c||f?(a=f?d:c?b:a,this.tokens.push({index:this.index,text:a,operator:!0}),this.index+=a.length):this.throwError("Unexpected next character ",this.index,this.index+1)}return this.tokens},is:function(a,b){return-1!==b.indexOf(a)},peek:function(a){a=a||1;return this.index+a<this.text.length?this.text.charAt(this.index+a):!1},isNumber:function(a){return"0"<=a&&"9">=a&&"string"===
typeof a},isWhitespace:function(a){return" "===a||"\r"===a||"\t"===a||"\n"===a||"\v"===a||"\u00a0"===a},isIdentifierStart:function(a){return this.options.isIdentifierStart?this.options.isIdentifierStart(a,this.codePointAt(a)):this.isValidIdentifierStart(a)},isValidIdentifierStart:function(a){return"a"<=a&&"z">=a||"A"<=a&&"Z">=a||"_"===a||"$"===a},isIdentifierContinue:function(a){return this.options.isIdentifierContinue?this.options.isIdentifierContinue(a,this.codePointAt(a)):this.isValidIdentifierContinue(a)},
isValidIdentifierContinue:function(a,b){return this.isValidIdentifierStart(a,b)||this.isNumber(a)},codePointAt:function(a){return 1===a.length?a.charCodeAt(0):(a.charCodeAt(0)<<10)+a.charCodeAt(1)-56613888},peekMultichar:function(){var a=this.text.charAt(this.index),b=this.peek();if(!b)return a;var d=a.charCodeAt(0),c=b.charCodeAt(0);return 55296<=d&&56319>=d&&56320<=c&&57343>=c?a+b:a},isExpOperator:function(a){return"-"===a||"+"===a||this.isNumber(a)},throwError:function(a,b,d){d=d||this.index;b=
x(b)?"s "+b+"-"+this.index+" ["+this.text.substring(b,d)+"]":" "+d;throw ea("lexerr",a,b,this.text);},readNumber:function(){for(var a="",b=this.index;this.index<this.text.length;){var d=Q(this.text.charAt(this.index));if("."===d||this.isNumber(d))a+=d;else{var c=this.peek();if("e"===d&&this.isExpOperator(c))a+=d;else if(this.isExpOperator(d)&&c&&this.isNumber(c)&&"e"===a.charAt(a.length-1))a+=d;else if(!this.isExpOperator(d)||c&&this.isNumber(c)||"e"!==a.charAt(a.length-1))break;else this.throwError("Invalid exponent")}this.index++}this.tokens.push({index:b,
text:a,constant:!0,value:Number(a)})},readIdent:function(){var a=this.index;for(this.index+=this.peekMultichar().length;this.index<this.text.length;){var b=this.peekMultichar();if(!this.isIdentifierContinue(b))break;this.index+=b.length}this.tokens.push({index:a,text:this.text.slice(a,this.index),identifier:!0})},readString:function(a){var b=this.index;this.index++;for(var d="",c=a,f=!1;this.index<this.text.length;){var e=this.text.charAt(this.index),c=c+e;if(f)"u"===e?(f=this.text.substring(this.index+
1,this.index+5),f.match(/[\da-f]{4}/i)||this.throwError("Invalid unicode escape [\\u"+f+"]"),this.index+=4,d+=String.fromCharCode(parseInt(f,16))):d+=bh[e]||e,f=!1;else if("\\"===e)f=!0;else{if(e===a){this.index++;this.tokens.push({index:b,text:c,constant:!0,value:d});return}d+=e}this.index++}this.throwError("Unterminated quote",b)}};var t=function(a,b){this.lexer=a;this.options=b};t.Program="Program";t.ExpressionStatement="ExpressionStatement";t.AssignmentExpression="AssignmentExpression";t.ConditionalExpression=
"ConditionalExpression";t.LogicalExpression="LogicalExpression";t.BinaryExpression="BinaryExpression";t.UnaryExpression="UnaryExpression";t.CallExpression="CallExpression";t.MemberExpression="MemberExpression";t.Identifier="Identifier";t.Literal="Literal";t.ArrayExpression="ArrayExpression";t.Property="Property";t.ObjectExpression="ObjectExpression";t.ThisExpression="ThisExpression";t.LocalsExpression="LocalsExpression";t.NGValueParameter="NGValueParameter";t.prototype={ast:function(a){this.text=
a;this.tokens=this.lexer.lex(a);a=this.program();0!==this.tokens.length&&this.throwError("is an unexpected token",this.tokens[0]);return a},program:function(){for(var a=[];;)if(0<this.tokens.length&&!this.peek("}",")",";","]")&&a.push(this.expressionStatement()),!this.expect(";"))return{type:t.Program,body:a}},expressionStatement:function(){return{type:t.ExpressionStatement,expression:this.filterChain()}},filterChain:function(){for(var a=this.expression();this.expect("|");)a=this.filter(a);return a},
expression:function(){return this.assignment()},assignment:function(){var a=this.ternary();if(this.expect("=")){if(!Dd(a))throw ea("lval");a={type:t.AssignmentExpression,left:a,right:this.assignment(),operator:"="}}return a},ternary:function(){var a=this.logicalOR(),b,d;return this.expect("?")&&(b=this.expression(),this.consume(":"))?(d=this.expression(),{type:t.ConditionalExpression,test:a,alternate:b,consequent:d}):a},logicalOR:function(){for(var a=this.logicalAND();this.expect("||");)a={type:t.LogicalExpression,
operator:"||",left:a,right:this.logicalAND()};return a},logicalAND:function(){for(var a=this.equality();this.expect("&&");)a={type:t.LogicalExpression,operator:"&&",left:a,right:this.equality()};return a},equality:function(){for(var a=this.relational(),b;b=this.expect("==","!=","===","!==");)a={type:t.BinaryExpression,operator:b.text,left:a,right:this.relational()};return a},relational:function(){for(var a=this.additive(),b;b=this.expect("<",">","<=",">=");)a={type:t.BinaryExpression,operator:b.text,
left:a,right:this.additive()};return a},additive:function(){for(var a=this.multiplicative(),b;b=this.expect("+","-");)a={type:t.BinaryExpression,operator:b.text,left:a,right:this.multiplicative()};return a},multiplicative:function(){for(var a=this.unary(),b;b=this.expect("*","/","%");)a={type:t.BinaryExpression,operator:b.text,left:a,right:this.unary()};return a},unary:function(){var a;return(a=this.expect("+","-","!"))?{type:t.UnaryExpression,operator:a.text,prefix:!0,argument:this.unary()}:this.primary()},
primary:function(){var a;this.expect("(")?(a=this.filterChain(),this.consume(")")):this.expect("[")?a=this.arrayDeclaration():this.expect("{")?a=this.object():this.selfReferential.hasOwnProperty(this.peek().text)?a=sa(this.selfReferential[this.consume().text]):this.options.literals.hasOwnProperty(this.peek().text)?a={type:t.Literal,value:this.options.literals[this.consume().text]}:this.peek().identifier?a=this.identifier():this.peek().constant?a=this.constant():this.throwError("not a primary expression",
this.peek());for(var b;b=this.expect("(","[",".");)"("===b.text?(a={type:t.CallExpression,callee:a,arguments:this.parseArguments()},this.consume(")")):"["===b.text?(a={type:t.MemberExpression,object:a,property:this.expression(),computed:!0},this.consume("]")):"."===b.text?a={type:t.MemberExpression,object:a,property:this.identifier(),computed:!1}:this.throwError("IMPOSSIBLE");return a},filter:function(a){a=[a];for(var b={type:t.CallExpression,callee:this.identifier(),arguments:a,filter:!0};this.expect(":");)a.push(this.expression());
return b},parseArguments:function(){var a=[];if(")"!==this.peekToken().text){do a.push(this.filterChain());while(this.expect(","))}return a},identifier:function(){var a=this.consume();a.identifier||this.throwError("is not a valid identifier",a);return{type:t.Identifier,name:a.text}},constant:function(){return{type:t.Literal,value:this.consume().value}},arrayDeclaration:function(){var a=[];if("]"!==this.peekToken().text){do{if(this.peek("]"))break;a.push(this.expression())}while(this.expect(","))}this.consume("]");
return{type:t.ArrayExpression,elements:a}},object:function(){var a=[],b;if("}"!==this.peekToken().text){do{if(this.peek("}"))break;b={type:t.Property,kind:"init"};this.peek().constant?(b.key=this.constant(),b.computed=!1,this.consume(":"),b.value=this.expression()):this.peek().identifier?(b.key=this.identifier(),b.computed=!1,this.peek(":")?(this.consume(":"),b.value=this.expression()):b.value=b.key):this.peek("[")?(this.consume("["),b.key=this.expression(),this.consume("]"),b.computed=!0,this.consume(":"),
b.value=this.expression()):this.throwError("invalid key",this.peek());a.push(b)}while(this.expect(","))}this.consume("}");return{type:t.ObjectExpression,properties:a}},throwError:function(a,b){throw ea("syntax",b.text,a,b.index+1,this.text,this.text.substring(b.index));},consume:function(a){if(0===this.tokens.length)throw ea("ueoe",this.text);var b=this.expect(a);b||this.throwError("is unexpected, expecting ["+a+"]",this.peek());return b},peekToken:function(){if(0===this.tokens.length)throw ea("ueoe",
this.text);return this.tokens[0]},peek:function(a,b,d,c){return this.peekAhead(0,a,b,d,c)},peekAhead:function(a,b,d,c,f){if(this.tokens.length>a){a=this.tokens[a];var e=a.text;if(e===b||e===d||e===c||e===f||!(b||d||c||f))return a}return!1},expect:function(a,b,d,c){return(a=this.peek(a,b,d,c))?(this.tokens.shift(),a):!1},selfReferential:{"this":{type:t.ThisExpression},$locals:{type:t.LocalsExpression}}};Gd.prototype={compile:function(a,b){var d=this,c=this.astBuilder.ast(a);this.state={nextId:0,filters:{},
expensiveChecks:b,fn:{vars:[],body:[],own:{}},assign:{vars:[],body:[],own:{}},inputs:[]};X(c,d.$filter);var f="",e;this.stage="assign";if(e=Ed(c))this.state.computing="assign",f=this.nextId(),this.recurse(e,f),this.return_(f),f="fn.assign="+this.generateFunction("assign","s,v,l");e=Cd(c.body);d.stage="inputs";q(e,function(a,b){var c="fn"+b;d.state[c]={vars:[],body:[],own:{}};d.state.computing=c;var e=d.nextId();d.recurse(a,e);d.return_(e);d.state.inputs.push(c);a.watchId=b});this.state.computing=
"fn";this.stage="main";this.recurse(c);f='"'+this.USE+" "+this.STRICT+'";\n'+this.filterPrefix()+"var fn="+this.generateFunction("fn","s,l,a,i")+f+this.watchFns()+"return fn;";f=(new Function("$filter","ensureSafeMemberName","ensureSafeObject","ensureSafeFunction","getStringValue","ensureSafeAssignContext","ifDefined","plus","text",f))(this.$filter,Ua,Ea,td,wg,Jb,Eg,Bd,a);this.state=this.stage=void 0;f.literal=Fd(c);f.constant=c.constant;return f},USE:"use",STRICT:"strict",watchFns:function(){var a=
[],b=this.state.inputs,d=this;q(b,function(b){a.push("var "+b+"="+d.generateFunction(b,"s"))});b.length&&a.push("fn.inputs=["+b.join(",")+"];");return a.join("")},generateFunction:function(a,b){return"function("+b+"){"+this.varsPrefix(a)+this.body(a)+"};"},filterPrefix:function(){var a=[],b=this;q(this.state.filters,function(d,c){a.push(d+"=$filter("+b.escape(c)+")")});return a.length?"var "+a.join(",")+";":""},varsPrefix:function(a){return this.state[a].vars.length?"var "+this.state[a].vars.join(",")+
";":""},body:function(a){return this.state[a].body.join("")},recurse:function(a,b,d,c,f,e){var g,h,k=this,l,m,n;c=c||w;if(!e&&x(a.watchId))b=b||this.nextId(),this.if_("i",this.lazyAssign(b,this.computedMember("i",a.watchId)),this.lazyRecurse(a,b,d,c,f,!0));else switch(a.type){case t.Program:q(a.body,function(b,c){k.recurse(b.expression,void 0,void 0,function(a){h=a});c!==a.body.length-1?k.current().body.push(h,";"):k.return_(h)});break;case t.Literal:m=this.escape(a.value);this.assign(b,m);c(m);break;
case t.UnaryExpression:this.recurse(a.argument,void 0,void 0,function(a){h=a});m=a.operator+"("+this.ifDefined(h,0)+")";this.assign(b,m);c(m);break;case t.BinaryExpression:this.recurse(a.left,void 0,void 0,function(a){g=a});this.recurse(a.right,void 0,void 0,function(a){h=a});m="+"===a.operator?this.plus(g,h):"-"===a.operator?this.ifDefined(g,0)+a.operator+this.ifDefined(h,0):"("+g+")"+a.operator+"("+h+")";this.assign(b,m);c(m);break;case t.LogicalExpression:b=b||this.nextId();k.recurse(a.left,b);
k.if_("&&"===a.operator?b:k.not(b),k.lazyRecurse(a.right,b));c(b);break;case t.ConditionalExpression:b=b||this.nextId();k.recurse(a.test,b);k.if_(b,k.lazyRecurse(a.alternate,b),k.lazyRecurse(a.consequent,b));c(b);break;case t.Identifier:b=b||this.nextId();d&&(d.context="inputs"===k.stage?"s":this.assign(this.nextId(),this.getHasOwnProperty("l",a.name)+"?l:s"),d.computed=!1,d.name=a.name);Ua(a.name);k.if_("inputs"===k.stage||k.not(k.getHasOwnProperty("l",a.name)),function(){k.if_("inputs"===k.stage||
"s",function(){f&&1!==f&&k.if_(k.not(k.nonComputedMember("s",a.name)),k.lazyAssign(k.nonComputedMember("s",a.name),"{}"));k.assign(b,k.nonComputedMember("s",a.name))})},b&&k.lazyAssign(b,k.nonComputedMember("l",a.name)));(k.state.expensiveChecks||Lb(a.name))&&k.addEnsureSafeObject(b);c(b);break;case t.MemberExpression:g=d&&(d.context=this.nextId())||this.nextId();b=b||this.nextId();k.recurse(a.object,g,void 0,function(){k.if_(k.notNull(g),function(){f&&1!==f&&k.addEnsureSafeAssignContext(g);if(a.computed)h=
k.nextId(),k.recurse(a.property,h),k.getStringValue(h),k.addEnsureSafeMemberName(h),f&&1!==f&&k.if_(k.not(k.computedMember(g,h)),k.lazyAssign(k.computedMember(g,h),"{}")),m=k.ensureSafeObject(k.computedMember(g,h)),k.assign(b,m),d&&(d.computed=!0,d.name=h);else{Ua(a.property.name);f&&1!==f&&k.if_(k.not(k.nonComputedMember(g,a.property.name)),k.lazyAssign(k.nonComputedMember(g,a.property.name),"{}"));m=k.nonComputedMember(g,a.property.name);if(k.state.expensiveChecks||Lb(a.property.name))m=k.ensureSafeObject(m);
k.assign(b,m);d&&(d.computed=!1,d.name=a.property.name)}},function(){k.assign(b,"undefined")});c(b)},!!f);break;case t.CallExpression:b=b||this.nextId();a.filter?(h=k.filter(a.callee.name),l=[],q(a.arguments,function(a){var b=k.nextId();k.recurse(a,b);l.push(b)}),m=h+"("+l.join(",")+")",k.assign(b,m),c(b)):(h=k.nextId(),g={},l=[],k.recurse(a.callee,h,g,function(){k.if_(k.notNull(h),function(){k.addEnsureSafeFunction(h);q(a.arguments,function(a){k.recurse(a,k.nextId(),void 0,function(a){l.push(k.ensureSafeObject(a))})});
g.name?(k.state.expensiveChecks||k.addEnsureSafeObject(g.context),m=k.member(g.context,g.name,g.computed)+"("+l.join(",")+")"):m=h+"("+l.join(",")+")";m=k.ensureSafeObject(m);k.assign(b,m)},function(){k.assign(b,"undefined")});c(b)}));break;case t.AssignmentExpression:h=this.nextId();g={};this.recurse(a.left,void 0,g,function(){k.if_(k.notNull(g.context),function(){k.recurse(a.right,h);k.addEnsureSafeObject(k.member(g.context,g.name,g.computed));k.addEnsureSafeAssignContext(g.context);m=k.member(g.context,
g.name,g.computed)+a.operator+h;k.assign(b,m);c(b||m)})},1);break;case t.ArrayExpression:l=[];q(a.elements,function(a){k.recurse(a,k.nextId(),void 0,function(a){l.push(a)})});m="["+l.join(",")+"]";this.assign(b,m);c(m);break;case t.ObjectExpression:l=[];n=!1;q(a.properties,function(a){a.computed&&(n=!0)});n?(b=b||this.nextId(),this.assign(b,"{}"),q(a.properties,function(a){a.computed?(g=k.nextId(),k.recurse(a.key,g)):g=a.key.type===t.Identifier?a.key.name:""+a.key.value;h=k.nextId();k.recurse(a.value,
h);k.assign(k.member(b,g,a.computed),h)})):(q(a.properties,function(b){k.recurse(b.value,a.constant?void 0:k.nextId(),void 0,function(a){l.push(k.escape(b.key.type===t.Identifier?b.key.name:""+b.key.value)+":"+a)})}),m="{"+l.join(",")+"}",this.assign(b,m));c(b||m);break;case t.ThisExpression:this.assign(b,"s");c("s");break;case t.LocalsExpression:this.assign(b,"l");c("l");break;case t.NGValueParameter:this.assign(b,"v"),c("v")}},getHasOwnProperty:function(a,b){var d=a+"."+b,c=this.current().own;c.hasOwnProperty(d)||
(c[d]=this.nextId(!1,a+"&&("+this.escape(b)+" in "+a+")"));return c[d]},assign:function(a,b){if(a)return this.current().body.push(a,"=",b,";"),a},filter:function(a){this.state.filters.hasOwnProperty(a)||(this.state.filters[a]=this.nextId(!0));return this.state.filters[a]},ifDefined:function(a,b){return"ifDefined("+a+","+this.escape(b)+")"},plus:function(a,b){return"plus("+a+","+b+")"},return_:function(a){this.current().body.push("return ",a,";")},if_:function(a,b,d){if(!0===a)b();else{var c=this.current().body;
c.push("if(",a,"){");b();c.push("}");d&&(c.push("else{"),d(),c.push("}"))}},not:function(a){return"!("+a+")"},notNull:function(a){return a+"!=null"},nonComputedMember:function(a,b){var d=/[^$_a-zA-Z0-9]/g;return/^[$_a-zA-Z][$_a-zA-Z0-9]*$/.test(b)?a+"."+b:a+'["'+b.replace(d,this.stringEscapeFn)+'"]'},computedMember:function(a,b){return a+"["+b+"]"},member:function(a,b,d){return d?this.computedMember(a,b):this.nonComputedMember(a,b)},addEnsureSafeObject:function(a){this.current().body.push(this.ensureSafeObject(a),
";")},addEnsureSafeMemberName:function(a){this.current().body.push(this.ensureSafeMemberName(a),";")},addEnsureSafeFunction:function(a){this.current().body.push(this.ensureSafeFunction(a),";")},addEnsureSafeAssignContext:function(a){this.current().body.push(this.ensureSafeAssignContext(a),";")},ensureSafeObject:function(a){return"ensureSafeObject("+a+",text)"},ensureSafeMemberName:function(a){return"ensureSafeMemberName("+a+",text)"},ensureSafeFunction:function(a){return"ensureSafeFunction("+a+",text)"},
getStringValue:function(a){this.assign(a,"getStringValue("+a+")")},ensureSafeAssignContext:function(a){return"ensureSafeAssignContext("+a+",text)"},lazyRecurse:function(a,b,d,c,f,e){var g=this;return function(){g.recurse(a,b,d,c,f,e)}},lazyAssign:function(a,b){var d=this;return function(){d.assign(a,b)}},stringEscapeRegex:/[^ a-zA-Z0-9]/g,stringEscapeFn:function(a){return"\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)},escape:function(a){if(D(a))return"'"+a.replace(this.stringEscapeRegex,this.stringEscapeFn)+
"'";if(ba(a))return a.toString();if(!0===a)return"true";if(!1===a)return"false";if(null===a)return"null";if("undefined"===typeof a)return"undefined";throw ea("esc");},nextId:function(a,b){var d="v"+this.state.nextId++;a||this.current().vars.push(d+(b?"="+b:""));return d},current:function(){return this.state[this.state.computing]}};Hd.prototype={compile:function(a,b){var d=this,c=this.astBuilder.ast(a);this.expression=a;this.expensiveChecks=b;X(c,d.$filter);var f,e;if(f=Ed(c))e=this.recurse(f);f=Cd(c.body);
var g;f&&(g=[],q(f,function(a,b){var c=d.recurse(a);a.input=c;g.push(c);a.watchId=b}));var h=[];q(c.body,function(a){h.push(d.recurse(a.expression))});f=0===c.body.length?w:1===c.body.length?h[0]:function(a,b){var c;q(h,function(d){c=d(a,b)});return c};e&&(f.assign=function(a,b,c){return e(a,c,b)});g&&(f.inputs=g);f.literal=Fd(c);f.constant=c.constant;return f},recurse:function(a,b,d){var c,f,e=this,g;if(a.input)return this.inputs(a.input,a.watchId);switch(a.type){case t.Literal:return this.value(a.value,
b);case t.UnaryExpression:return f=this.recurse(a.argument),this["unary"+a.operator](f,b);case t.BinaryExpression:return c=this.recurse(a.left),f=this.recurse(a.right),this["binary"+a.operator](c,f,b);case t.LogicalExpression:return c=this.recurse(a.left),f=this.recurse(a.right),this["binary"+a.operator](c,f,b);case t.ConditionalExpression:return this["ternary?:"](this.recurse(a.test),this.recurse(a.alternate),this.recurse(a.consequent),b);case t.Identifier:return Ua(a.name,e.expression),e.identifier(a.name,
e.expensiveChecks||Lb(a.name),b,d,e.expression);case t.MemberExpression:return c=this.recurse(a.object,!1,!!d),a.computed||(Ua(a.property.name,e.expression),f=a.property.name),a.computed&&(f=this.recurse(a.property)),a.computed?this.computedMember(c,f,b,d,e.expression):this.nonComputedMember(c,f,e.expensiveChecks,b,d,e.expression);case t.CallExpression:return g=[],q(a.arguments,function(a){g.push(e.recurse(a))}),a.filter&&(f=this.$filter(a.callee.name)),a.filter||(f=this.recurse(a.callee,!0)),a.filter?
function(a,c,d,e){for(var n=[],r=0;r<g.length;++r)n.push(g[r](a,c,d,e));a=f.apply(void 0,n,e);return b?{context:void 0,name:void 0,value:a}:a}:function(a,c,d,m){var n=f(a,c,d,m),r;if(null!=n.value){Ea(n.context,e.expression);td(n.value,e.expression);r=[];for(var s=0;s<g.length;++s)r.push(Ea(g[s](a,c,d,m),e.expression));r=Ea(n.value.apply(n.context,r),e.expression)}return b?{value:r}:r};case t.AssignmentExpression:return c=this.recurse(a.left,!0,1),f=this.recurse(a.right),function(a,d,g,m){var n=c(a,
d,g,m);a=f(a,d,g,m);Ea(n.value,e.expression);Jb(n.context);n.context[n.name]=a;return b?{value:a}:a};case t.ArrayExpression:return g=[],q(a.elements,function(a){g.push(e.recurse(a))}),function(a,c,d,e){for(var f=[],r=0;r<g.length;++r)f.push(g[r](a,c,d,e));return b?{value:f}:f};case t.ObjectExpression:return g=[],q(a.properties,function(a){a.computed?g.push({key:e.recurse(a.key),computed:!0,value:e.recurse(a.value)}):g.push({key:a.key.type===t.Identifier?a.key.name:""+a.key.value,computed:!1,value:e.recurse(a.value)})}),
function(a,c,d,e){for(var f={},r=0;r<g.length;++r)g[r].computed?f[g[r].key(a,c,d,e)]=g[r].value(a,c,d,e):f[g[r].key]=g[r].value(a,c,d,e);return b?{value:f}:f};case t.ThisExpression:return function(a){return b?{value:a}:a};case t.LocalsExpression:return function(a,c){return b?{value:c}:c};case t.NGValueParameter:return function(a,c,d){return b?{value:d}:d}}},"unary+":function(a,b){return function(d,c,f,e){d=a(d,c,f,e);d=x(d)?+d:0;return b?{value:d}:d}},"unary-":function(a,b){return function(d,c,f,
e){d=a(d,c,f,e);d=x(d)?-d:0;return b?{value:d}:d}},"unary!":function(a,b){return function(d,c,f,e){d=!a(d,c,f,e);return b?{value:d}:d}},"binary+":function(a,b,d){return function(c,f,e,g){var h=a(c,f,e,g);c=b(c,f,e,g);h=Bd(h,c);return d?{value:h}:h}},"binary-":function(a,b,d){return function(c,f,e,g){var h=a(c,f,e,g);c=b(c,f,e,g);h=(x(h)?h:0)-(x(c)?c:0);return d?{value:h}:h}},"binary*":function(a,b,d){return function(c,f,e,g){c=a(c,f,e,g)*b(c,f,e,g);return d?{value:c}:c}},"binary/":function(a,b,d){return function(c,
f,e,g){c=a(c,f,e,g)/b(c,f,e,g);return d?{value:c}:c}},"binary%":function(a,b,d){return function(c,f,e,g){c=a(c,f,e,g)%b(c,f,e,g);return d?{value:c}:c}},"binary===":function(a,b,d){return function(c,f,e,g){c=a(c,f,e,g)===b(c,f,e,g);return d?{value:c}:c}},"binary!==":function(a,b,d){return function(c,f,e,g){c=a(c,f,e,g)!==b(c,f,e,g);return d?{value:c}:c}},"binary==":function(a,b,d){return function(c,f,e,g){c=a(c,f,e,g)==b(c,f,e,g);return d?{value:c}:c}},"binary!=":function(a,b,d){return function(c,
f,e,g){c=a(c,f,e,g)!=b(c,f,e,g);return d?{value:c}:c}},"binary<":function(a,b,d){return function(c,f,e,g){c=a(c,f,e,g)<b(c,f,e,g);return d?{value:c}:c}},"binary>":function(a,b,d){return function(c,f,e,g){c=a(c,f,e,g)>b(c,f,e,g);return d?{value:c}:c}},"binary<=":function(a,b,d){return function(c,f,e,g){c=a(c,f,e,g)<=b(c,f,e,g);return d?{value:c}:c}},"binary>=":function(a,b,d){return function(c,f,e,g){c=a(c,f,e,g)>=b(c,f,e,g);return d?{value:c}:c}},"binary&&":function(a,b,d){return function(c,f,e,g){c=
a(c,f,e,g)&&b(c,f,e,g);return d?{value:c}:c}},"binary||":function(a,b,d){return function(c,f,e,g){c=a(c,f,e,g)||b(c,f,e,g);return d?{value:c}:c}},"ternary?:":function(a,b,d,c){return function(f,e,g,h){f=a(f,e,g,h)?b(f,e,g,h):d(f,e,g,h);return c?{value:f}:f}},value:function(a,b){return function(){return b?{context:void 0,name:void 0,value:a}:a}},identifier:function(a,b,d,c,f){return function(e,g,h,k){e=g&&a in g?g:e;c&&1!==c&&e&&!e[a]&&(e[a]={});g=e?e[a]:void 0;b&&Ea(g,f);return d?{context:e,name:a,
value:g}:g}},computedMember:function(a,b,d,c,f){return function(e,g,h,k){var l=a(e,g,h,k),m,n;null!=l&&(m=b(e,g,h,k),m+="",Ua(m,f),c&&1!==c&&(Jb(l),l&&!l[m]&&(l[m]={})),n=l[m],Ea(n,f));return d?{context:l,name:m,value:n}:n}},nonComputedMember:function(a,b,d,c,f,e){return function(g,h,k,l){g=a(g,h,k,l);f&&1!==f&&(Jb(g),g&&!g[b]&&(g[b]={}));h=null!=g?g[b]:void 0;(d||Lb(b))&&Ea(h,e);return c?{context:g,name:b,value:h}:h}},inputs:function(a,b){return function(d,c,f,e){return e?e[b]:a(d,c,f)}}};var nc=
function(a,b,d){this.lexer=a;this.$filter=b;this.options=d;this.ast=new t(a,d);this.astCompiler=d.csp?new Hd(this.ast,b):new Gd(this.ast,b)};nc.prototype={constructor:nc,parse:function(a){return this.astCompiler.compile(a,this.options.expensiveChecks)}};var Fa=G("$sce"),ga={HTML:"html",CSS:"css",URL:"url",RESOURCE_URL:"resourceUrl",JS:"js"},Hg=G("$compile"),aa=y.document.createElement("a"),Ld=ta(y.location.href);Md.$inject=["$document"];Rc.$inject=["$provide"];var Td=22,Sd=".",pc="0";Nd.$inject=["$locale"];
Pd.$inject=["$locale"];var Sg={yyyy:U("FullYear",4,0,!1,!0),yy:U("FullYear",2,0,!0,!0),y:U("FullYear",1,0,!1,!0),MMMM:nb("Month"),MMM:nb("Month",!0),MM:U("Month",2,1),M:U("Month",1,1),LLLL:nb("Month",!1,!0),dd:U("Date",2),d:U("Date",1),HH:U("Hours",2),H:U("Hours",1),hh:U("Hours",2,-12),h:U("Hours",1,-12),mm:U("Minutes",2),m:U("Minutes",1),ss:U("Seconds",2),s:U("Seconds",1),sss:U("Milliseconds",3),EEEE:nb("Day"),EEE:nb("Day",!0),a:function(a,b){return 12>a.getHours()?b.AMPMS[0]:b.AMPMS[1]},Z:function(a,
b,d){a=-1*d;return a=(0<=a?"+":"")+(Mb(Math[0<a?"floor":"ceil"](a/60),2)+Mb(Math.abs(a%60),2))},ww:Vd(2),w:Vd(1),G:qc,GG:qc,GGG:qc,GGGG:function(a,b){return 0>=a.getFullYear()?b.ERANAMES[0]:b.ERANAMES[1]}},Rg=/((?:[^yMLdHhmsaZEwG']+)|(?:'(?:[^']|'')*')|(?:E+|y+|M+|L+|d+|H+|h+|m+|s+|a|Z|G+|w+))(.*)/,Qg=/^-?\d+$/;Od.$inject=["$locale"];var Lg=ha(Q),Mg=ha(wb);Qd.$inject=["$parse"];var Ce=ha({restrict:"E",compile:function(a,b){if(!b.href&&!b.xlinkHref)return function(a,b){if("a"===b[0].nodeName.toLowerCase()){var f=
"[object SVGAnimatedString]"===ma.call(b.prop("href"))?"xlink:href":"href";b.on("click",function(a){b.attr(f)||a.preventDefault()})}}}}),xb={};q(Gb,function(a,b){function d(a,d,f){a.$watch(f[c],function(a){f.$set(b,!!a)})}if("multiple"!==a){var c=Da("ng-"+b),f=d;"checked"===a&&(f=function(a,b,f){f.ngModel!==f[c]&&d(a,b,f)});xb[c]=function(){return{restrict:"A",priority:100,link:f}}}});q(gd,function(a,b){xb[b]=function(){return{priority:100,link:function(a,c,f){if("ngPattern"===b&&"/"===f.ngPattern.charAt(0)&&
(c=f.ngPattern.match(Vg))){f.$set("ngPattern",new RegExp(c[1],c[2]));return}a.$watch(f[b],function(a){f.$set(b,a)})}}}});q(["src","srcset","href"],function(a){var b=Da("ng-"+a);xb[b]=function(){return{priority:99,link:function(d,c,f){var e=a,g=a;"href"===a&&"[object SVGAnimatedString]"===ma.call(c.prop("href"))&&(g="xlinkHref",f.$attr[g]="xlink:href",e=null);f.$observe(b,function(b){b?(f.$set(g,b),Ia&&e&&c.prop(e,f[g])):"href"===a&&f.$set(g,null)})}}}});var Nb={$addControl:w,$$renameControl:function(a,
b){a.$name=b},$removeControl:w,$setValidity:w,$setDirty:w,$setPristine:w,$setSubmitted:w};Wd.$inject=["$element","$attrs","$scope","$animate","$interpolate"];var ee=function(a){return["$timeout","$parse",function(b,d){function c(a){return""===a?d('this[""]').assign:d(a).assign||w}return{name:"form",restrict:a?"EAC":"E",require:["form","^^?form"],controller:Wd,compile:function(d,e){d.addClass(Wa).addClass(rb);var g=e.name?"name":a&&e.ngForm?"ngForm":!1;return{pre:function(a,d,e,f){var n=f[0];if(!("action"in
e)){var r=function(b){a.$apply(function(){n.$commitViewValue();n.$setSubmitted()});b.preventDefault()};d[0].addEventListener("submit",r,!1);d.on("$destroy",function(){b(function(){d[0].removeEventListener("submit",r,!1)},0,!1)})}(f[1]||n.$$parentForm).$addControl(n);var s=g?c(n.$name):w;g&&(s(a,n),e.$observe(g,function(b){n.$name!==b&&(s(a,void 0),n.$$parentForm.$$renameControl(n,b),s=c(n.$name),s(a,n))}));d.on("$destroy",function(){n.$$parentForm.$removeControl(n);s(a,void 0);R(n,Nb)})}}}}}]},De=
ee(),Pe=ee(!0),Tg=/^\d{4,}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+(?:[+-][0-2]\d:[0-5]\d|Z)$/,ch=/^[a-z][a-z\d.+-]*:\/*(?:[^:@]+(?::[^@]+)?@)?(?:[^\s:/?#]+|\[[a-f\d:]+])(?::\d+)?(?:\/[^?#]*)?(?:\?[^#]*)?(?:#.*)?$/i,dh=/^(?=.{1,254}$)(?=.{1,64}@)[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+(\.[-!#$%&'*+/0-9=?A-Z^_`a-z{|}~]+)*@[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?(\.[A-Za-z0-9]([A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*$/,Ug=/^\s*(-|\+)?(\d+|(\d*(\.\d*)))([eE][+-]?\d+)?\s*$/,fe=/^(\d{4,})-(\d{2})-(\d{2})$/,ge=/^(\d{4,})-(\d\d)-(\d\d)T(\d\d):(\d\d)(?::(\d\d)(\.\d{1,3})?)?$/,
wc=/^(\d{4,})-W(\d\d)$/,he=/^(\d{4,})-(\d\d)$/,ie=/^(\d\d):(\d\d)(?::(\d\d)(\.\d{1,3})?)?$/,Yd=V();q(["date","datetime-local","month","time","week"],function(a){Yd[a]=!0});var je={text:function(a,b,d,c,f,e){Xa(a,b,d,c,f,e);sc(c)},date:ob("date",fe,Pb(fe,["yyyy","MM","dd"]),"yyyy-MM-dd"),"datetime-local":ob("datetimelocal",ge,Pb(ge,"yyyy MM dd HH mm ss sss".split(" ")),"yyyy-MM-ddTHH:mm:ss.sss"),time:ob("time",ie,Pb(ie,["HH","mm","ss","sss"]),"HH:mm:ss.sss"),week:ob("week",wc,function(a,b){if(ja(a))return a;
if(D(a)){wc.lastIndex=0;var d=wc.exec(a);if(d){var c=+d[1],f=+d[2],e=d=0,g=0,h=0,k=Ud(c),f=7*(f-1);b&&(d=b.getHours(),e=b.getMinutes(),g=b.getSeconds(),h=b.getMilliseconds());return new Date(c,0,k.getDate()+f,d,e,g,h)}}return NaN},"yyyy-Www"),month:ob("month",he,Pb(he,["yyyy","MM"]),"yyyy-MM"),number:function(a,b,d,c,f,e){tc(a,b,d,c);Xa(a,b,d,c,f,e);Zd(c);var g,h;if(x(d.min)||d.ngMin)c.$validators.min=function(a){return c.$isEmpty(a)||z(g)||a>=g},d.$observe("min",function(a){g=qb(a);c.$validate()});
if(x(d.max)||d.ngMax)c.$validators.max=function(a){return c.$isEmpty(a)||z(h)||a<=h},d.$observe("max",function(a){h=qb(a);c.$validate()})},url:function(a,b,d,c,f,e){Xa(a,b,d,c,f,e);sc(c);c.$$parserName="url";c.$validators.url=function(a,b){var d=a||b;return c.$isEmpty(d)||ch.test(d)}},email:function(a,b,d,c,f,e){Xa(a,b,d,c,f,e);sc(c);c.$$parserName="email";c.$validators.email=function(a,b){var d=a||b;return c.$isEmpty(d)||dh.test(d)}},radio:function(a,b,d,c){z(d.name)&&b.attr("name",++sb);b.on("click",
function(a){b[0].checked&&c.$setViewValue(d.value,a&&a.type)});c.$render=function(){b[0].checked=d.value==c.$viewValue};d.$observe("value",c.$render)},range:function(a,b,d,c,f,e){function g(a,c){b.attr(a,d[a]);d.$observe(a,c)}function h(a){n=qb(a);ia(c.$modelValue)||(m?(a=b.val(),n>a&&(a=n,b.val(a)),c.$setViewValue(a)):c.$validate())}function k(a){r=qb(a);ia(c.$modelValue)||(m?(a=b.val(),r<a&&(b.val(r),a=r<n?n:r),c.$setViewValue(a)):c.$validate())}function l(a){s=qb(a);ia(c.$modelValue)||(m&&c.$viewValue!==
b.val()?c.$setViewValue(b.val()):c.$validate())}tc(a,b,d,c);Zd(c);Xa(a,b,d,c,f,e);var m=c.$$hasNativeValidators&&"range"===b[0].type,n=m?0:void 0,r=m?100:void 0,s=m?1:void 0,q=b[0].validity;a=x(d.min);f=x(d.max);e=x(d.step);var u=c.$render;c.$render=m&&x(q.rangeUnderflow)&&x(q.rangeOverflow)?function(){u();c.$setViewValue(b.val())}:u;a&&(c.$validators.min=m?function(){return!0}:function(a,b){return c.$isEmpty(b)||z(n)||b>=n},g("min",h));f&&(c.$validators.max=m?function(){return!0}:function(a,b){return c.$isEmpty(b)||
z(r)||b<=r},g("max",k));e&&(c.$validators.step=m?function(){return!q.stepMismatch}:function(a,b){var d;if(!(d=c.$isEmpty(b)||z(s))){d=n||0;var e=s,f=Number(b);if((f|0)!==f||(d|0)!==d||(e|0)!==e){var g=Math.max(uc(f),uc(d),uc(e)),g=Math.pow(10,g),f=f*g;d*=g;e*=g}d=0===(f-d)%e}return d},g("step",l))},checkbox:function(a,b,d,c,f,e,g,h){var k=$d(h,a,"ngTrueValue",d.ngTrueValue,!0),l=$d(h,a,"ngFalseValue",d.ngFalseValue,!1);b.on("click",function(a){c.$setViewValue(b[0].checked,a&&a.type)});c.$render=function(){b[0].checked=
c.$viewValue};c.$isEmpty=function(a){return!1===a};c.$formatters.push(function(a){return na(a,k)});c.$parsers.push(function(a){return a?k:l})},hidden:w,button:w,submit:w,reset:w,file:w},Lc=["$browser","$sniffer","$filter","$parse",function(a,b,d,c){return{restrict:"E",require:["?ngModel"],link:{pre:function(f,e,g,h){if(h[0]){var k=Q(g.type);"range"!==k||g.hasOwnProperty("ngInputRange")||(k="text");(je[k]||je.text)(f,e,g,h[0],b,a,d,c)}}}}}],eh=/^(true|false|\d+)$/,gf=function(){return{restrict:"A",
priority:100,compile:function(a,b){return eh.test(b.ngValue)?function(a,b,f){f.$set("value",a.$eval(f.ngValue))}:function(a,b,f){a.$watch(f.ngValue,function(a){f.$set("value",a)})}}}},He=["$compile",function(a){return{restrict:"AC",compile:function(b){a.$$addBindingClass(b);return function(b,c,f){a.$$addBindingInfo(c,f.ngBind);c=c[0];b.$watch(f.ngBind,function(a){c.textContent=z(a)?"":a})}}}}],Je=["$interpolate","$compile",function(a,b){return{compile:function(d){b.$$addBindingClass(d);return function(c,
d,e){c=a(d.attr(e.$attr.ngBindTemplate));b.$$addBindingInfo(d,c.expressions);d=d[0];e.$observe("ngBindTemplate",function(a){d.textContent=z(a)?"":a})}}}}],Ie=["$sce","$parse","$compile",function(a,b,d){return{restrict:"A",compile:function(c,f){var e=b(f.ngBindHtml),g=b(f.ngBindHtml,function(b){return a.valueOf(b)});d.$$addBindingClass(c);return function(b,c,f){d.$$addBindingInfo(c,f.ngBindHtml);b.$watch(g,function(){var d=e(b);c.html(a.getTrustedHtml(d)||"")})}}}}],ff=ha({restrict:"A",require:"ngModel",
link:function(a,b,d,c){c.$viewChangeListeners.push(function(){a.$eval(d.ngChange)})}}),Ke=vc("",!0),Me=vc("Odd",0),Le=vc("Even",1),Ne=Va({compile:function(a,b){b.$set("ngCloak",void 0);a.removeClass("ng-cloak")}}),Oe=[function(){return{restrict:"A",scope:!0,controller:"@",priority:500}}],Qc={},fh={blur:!0,focus:!0};q("click dblclick mousedown mouseup mouseover mouseout mousemove mouseenter mouseleave keydown keyup keypress submit focus blur copy cut paste".split(" "),function(a){var b=Da("ng-"+a);
Qc[b]=["$parse","$rootScope",function(d,c){return{restrict:"A",compile:function(f,e){var g=d(e[b],null,!0);return function(b,d){d.on(a,function(d){var e=function(){g(b,{$event:d})};fh[a]&&c.$$phase?b.$evalAsync(e):b.$apply(e)})}}}}]});var Re=["$animate","$compile",function(a,b){return{multiElement:!0,transclude:"element",priority:600,terminal:!0,restrict:"A",$$tlb:!0,link:function(d,c,f,e,g){var h,k,l;d.$watch(f.ngIf,function(d){d?k||g(function(d,e){k=e;d[d.length++]=b.$$createComment("end ngIf",
f.ngIf);h={clone:d};a.enter(d,c.parent(),c)}):(l&&(l.remove(),l=null),k&&(k.$destroy(),k=null),h&&(l=vb(h.clone),a.leave(l).done(function(a){!1!==a&&(l=null)}),h=null))})}}}],Se=["$templateRequest","$anchorScroll","$animate",function(a,b,d){return{restrict:"ECA",priority:400,terminal:!0,transclude:"element",controller:$.noop,compile:function(c,f){var e=f.ngInclude||f.src,g=f.onload||"",h=f.autoscroll;return function(c,f,m,n,r){var q=0,t,u,p,z=function(){u&&(u.remove(),u=null);t&&(t.$destroy(),t=null);
p&&(d.leave(p).done(function(a){!1!==a&&(u=null)}),u=p,p=null)};c.$watch(e,function(e){var m=function(a){!1===a||!x(h)||h&&!c.$eval(h)||b()},u=++q;e?(a(e,!0).then(function(a){if(!c.$$destroyed&&u===q){var b=c.$new();n.template=a;a=r(b,function(a){z();d.enter(a,null,f).done(m)});t=b;p=a;t.$emit("$includeContentLoaded",e);c.$eval(g)}},function(){c.$$destroyed||u!==q||(z(),c.$emit("$includeContentError",e))}),c.$emit("$includeContentRequested",e)):(z(),n.template=null)})}}}}],jf=["$compile",function(a){return{restrict:"ECA",
priority:-400,require:"ngInclude",link:function(b,d,c,f){ma.call(d[0]).match(/SVG/)?(d.empty(),a(Tc(f.template,y.document).childNodes)(b,function(a){d.append(a)},{futureParentElement:d})):(d.html(f.template),a(d.contents())(b))}}}],Te=Va({priority:450,compile:function(){return{pre:function(a,b,d){a.$eval(d.ngInit)}}}}),ef=function(){return{restrict:"A",priority:100,require:"ngModel",link:function(a,b,d,c){var f=b.attr(d.$attr.ngList)||", ",e="false"!==d.ngTrim,g=e?Y(f):f;c.$parsers.push(function(a){if(!z(a)){var b=
[];a&&q(a.split(g),function(a){a&&b.push(e?Y(a):a)});return b}});c.$formatters.push(function(a){if(I(a))return a.join(f)});c.$isEmpty=function(a){return!a||!a.length}}}},rb="ng-valid",ae="ng-invalid",Wa="ng-pristine",Ob="ng-dirty",ce="ng-pending",pb=G("ngModel"),gh=["$scope","$exceptionHandler","$attrs","$element","$parse","$animate","$timeout","$rootScope","$q","$interpolate",function(a,b,d,c,f,e,g,h,k,l){this.$modelValue=this.$viewValue=Number.NaN;this.$$rawModelValue=void 0;this.$validators={};
this.$asyncValidators={};this.$parsers=[];this.$formatters=[];this.$viewChangeListeners=[];this.$untouched=!0;this.$touched=!1;this.$pristine=!0;this.$dirty=!1;this.$valid=!0;this.$invalid=!1;this.$error={};this.$$success={};this.$pending=void 0;this.$name=l(d.name||"",!1)(a);this.$$parentForm=Nb;var m=f(d.ngModel),n=m.assign,r=m,s=n,t=null,u,p=this;this.$$setOptions=function(a){if((p.$options=a)&&a.getterSetter){var b=f(d.ngModel+"()"),e=f(d.ngModel+"($$$p)");r=function(a){var c=m(a);C(c)&&(c=b(a));
return c};s=function(a,b){C(m(a))?e(a,{$$$p:b}):n(a,b)}}else if(!m.assign)throw pb("nonassign",d.ngModel,ya(c));};this.$render=w;this.$isEmpty=function(a){return z(a)||""===a||null===a||a!==a};this.$$updateEmptyClasses=function(a){p.$isEmpty(a)?(e.removeClass(c,"ng-not-empty"),e.addClass(c,"ng-empty")):(e.removeClass(c,"ng-empty"),e.addClass(c,"ng-not-empty"))};var y=0;Xd({ctrl:this,$element:c,set:function(a,b){a[b]=!0},unset:function(a,b){delete a[b]},$animate:e});this.$setPristine=function(){p.$dirty=
!1;p.$pristine=!0;e.removeClass(c,Ob);e.addClass(c,Wa)};this.$setDirty=function(){p.$dirty=!0;p.$pristine=!1;e.removeClass(c,Wa);e.addClass(c,Ob);p.$$parentForm.$setDirty()};this.$setUntouched=function(){p.$touched=!1;p.$untouched=!0;e.setClass(c,"ng-untouched","ng-touched")};this.$setTouched=function(){p.$touched=!0;p.$untouched=!1;e.setClass(c,"ng-touched","ng-untouched")};this.$rollbackViewValue=function(){g.cancel(t);p.$viewValue=p.$$lastCommittedViewValue;p.$render()};this.$validate=function(){if(!ia(p.$modelValue)){var a=
p.$$rawModelValue,b=p.$valid,c=p.$modelValue,d=p.$options&&p.$options.allowInvalid;p.$$runValidators(a,p.$$lastCommittedViewValue,function(e){d||b===e||(p.$modelValue=e?a:void 0,p.$modelValue!==c&&p.$$writeModelToScope())})}};this.$$runValidators=function(a,b,c){function d(){var c=!0;q(p.$validators,function(d,e){var g=d(a,b);c=c&&g;f(e,g)});return c?!0:(q(p.$asyncValidators,function(a,b){f(b,null)}),!1)}function e(){var c=[],d=!0;q(p.$asyncValidators,function(e,g){var h=e(a,b);if(!h||!C(h.then))throw pb("nopromise",
h);f(g,void 0);c.push(h.then(function(){f(g,!0)},function(){d=!1;f(g,!1)}))});c.length?k.all(c).then(function(){g(d)},w):g(!0)}function f(a,b){h===y&&p.$setValidity(a,b)}function g(a){h===y&&c(a)}y++;var h=y;(function(){var a=p.$$parserName||"parse";if(z(u))f(a,null);else return u||(q(p.$validators,function(a,b){f(b,null)}),q(p.$asyncValidators,function(a,b){f(b,null)})),f(a,u),u;return!0})()?d()?e():g(!1):g(!1)};this.$commitViewValue=function(){var a=p.$viewValue;g.cancel(t);if(p.$$lastCommittedViewValue!==
a||""===a&&p.$$hasNativeValidators)p.$$updateEmptyClasses(a),p.$$lastCommittedViewValue=a,p.$pristine&&this.$setDirty(),this.$$parseAndValidate()};this.$$parseAndValidate=function(){var b=p.$$lastCommittedViewValue;if(u=z(b)?void 0:!0)for(var c=0;c<p.$parsers.length;c++)if(b=p.$parsers[c](b),z(b)){u=!1;break}ia(p.$modelValue)&&(p.$modelValue=r(a));var d=p.$modelValue,e=p.$options&&p.$options.allowInvalid;p.$$rawModelValue=b;e&&(p.$modelValue=b,p.$modelValue!==d&&p.$$writeModelToScope());p.$$runValidators(b,
p.$$lastCommittedViewValue,function(a){e||(p.$modelValue=a?b:void 0,p.$modelValue!==d&&p.$$writeModelToScope())})};this.$$writeModelToScope=function(){s(a,p.$modelValue);q(p.$viewChangeListeners,function(a){try{a()}catch(c){b(c)}})};this.$setViewValue=function(a,b){p.$viewValue=a;p.$options&&!p.$options.updateOnDefault||p.$$debounceViewValueCommit(b)};this.$$debounceViewValueCommit=function(b){var c=0,d=p.$options;d&&x(d.debounce)&&(d=d.debounce,ba(d)?c=d:ba(d[b])?c=d[b]:ba(d["default"])&&(c=d["default"]));
g.cancel(t);c?t=g(function(){p.$commitViewValue()},c):h.$$phase?p.$commitViewValue():a.$apply(function(){p.$commitViewValue()})};a.$watch(function(){var b=r(a);if(b!==p.$modelValue&&(p.$modelValue===p.$modelValue||b===b)){p.$modelValue=p.$$rawModelValue=b;u=void 0;for(var c=p.$formatters,d=c.length,e=b;d--;)e=c[d](e);p.$viewValue!==e&&(p.$$updateEmptyClasses(e),p.$viewValue=p.$$lastCommittedViewValue=e,p.$render(),p.$$runValidators(p.$modelValue,p.$viewValue,w))}return b})}],df=["$rootScope",function(a){return{restrict:"A",
require:["ngModel","^?form","^?ngModelOptions"],controller:gh,priority:1,compile:function(b){b.addClass(Wa).addClass("ng-untouched").addClass(rb);return{pre:function(a,b,f,e){var g=e[0];b=e[1]||g.$$parentForm;g.$$setOptions(e[2]&&e[2].$options);b.$addControl(g);f.$observe("name",function(a){g.$name!==a&&g.$$parentForm.$$renameControl(g,a)});a.$on("$destroy",function(){g.$$parentForm.$removeControl(g)})},post:function(b,c,f,e){var g=e[0];if(g.$options&&g.$options.updateOn)c.on(g.$options.updateOn,
function(a){g.$$debounceViewValueCommit(a&&a.type)});c.on("blur",function(){g.$touched||(a.$$phase?b.$evalAsync(g.$setTouched):b.$apply(g.$setTouched))})}}}}}],hh=/(\s+|^)default(\s+|$)/,hf=function(){return{restrict:"A",controller:["$scope","$attrs",function(a,b){var d=this;this.$options=sa(a.$eval(b.ngModelOptions));x(this.$options.updateOn)?(this.$options.updateOnDefault=!1,this.$options.updateOn=Y(this.$options.updateOn.replace(hh,function(){d.$options.updateOnDefault=!0;return" "}))):this.$options.updateOnDefault=
!0}]}},Ue=Va({terminal:!0,priority:1E3}),ih=G("ngOptions"),jh=/^\s*([\s\S]+?)(?:\s+as\s+([\s\S]+?))?(?:\s+group\s+by\s+([\s\S]+?))?(?:\s+disable\s+when\s+([\s\S]+?))?\s+for\s+(?:([$\w][$\w]*)|(?:\(\s*([$\w][$\w]*)\s*,\s*([$\w][$\w]*)\s*\)))\s+in\s+([\s\S]+?)(?:\s+track\s+by\s+([\s\S]+?))?$/,bf=["$compile","$document","$parse",function(a,b,d){function c(a,b,c){function e(a,b,c,d,f){this.selectValue=a;this.viewValue=b;this.label=c;this.group=d;this.disabled=f}function f(a){var b;if(!q&&la(a))b=a;else{b=
[];for(var c in a)a.hasOwnProperty(c)&&"$"!==c.charAt(0)&&b.push(c)}return b}var n=a.match(jh);if(!n)throw ih("iexp",a,ya(b));var r=n[5]||n[7],q=n[6];a=/ as /.test(n[0])&&n[1];var t=n[9];b=d(n[2]?n[1]:r);var u=a&&d(a)||b,p=t&&d(t),x=t?function(a,b){return p(c,b)}:function(a){return Aa(a)},A=function(a,b){return x(a,C(a,b))},v=d(n[2]||n[1]),z=d(n[3]||""),L=d(n[4]||""),w=d(n[8]),y={},C=q?function(a,b){y[q]=b;y[r]=a;return y}:function(a){y[r]=a;return y};return{trackBy:t,getTrackByValue:A,getWatchables:d(w,
function(a){var b=[];a=a||[];for(var d=f(a),e=d.length,g=0;g<e;g++){var h=a===d?g:d[g],l=a[h],h=C(l,h),l=x(l,h);b.push(l);if(n[2]||n[1])l=v(c,h),b.push(l);n[4]&&(h=L(c,h),b.push(h))}return b}),getOptions:function(){for(var a=[],b={},d=w(c)||[],g=f(d),h=g.length,n=0;n<h;n++){var p=d===g?n:g[n],r=C(d[p],p),q=u(c,r),p=x(q,r),s=v(c,r),y=z(c,r),r=L(c,r),q=new e(p,q,s,y,r);a.push(q);b[p]=q}return{items:a,selectValueMap:b,getOptionFromViewValue:function(a){return b[A(a)]},getViewValueFromOption:function(a){return t?
sa(a.viewValue):a.viewValue}}}}}var f=y.document.createElement("option"),e=y.document.createElement("optgroup");return{restrict:"A",terminal:!0,require:["select","ngModel"],link:{pre:function(a,b,c,d){d[0].registerOption=w},post:function(d,h,k,l){function m(a,b){a.element=b;b.disabled=a.disabled;a.label!==b.label&&(b.label=a.label,b.textContent=a.label);b.value=a.selectValue}function n(){var a=w&&r.readValue();if(w)for(var b=w.items.length-1;0<=b;b--){var c=w.items[b];x(c.group)?Fb(c.element.parentNode):
Fb(c.element)}w=C.getOptions();var d={};A&&h.prepend(u);w.items.forEach(function(a){var b;if(x(a.group)){b=d[a.group];b||(b=e.cloneNode(!1),D.appendChild(b),b.label=null===a.group?"null":a.group,d[a.group]=b);var c=f.cloneNode(!1)}else b=D,c=f.cloneNode(!1);b.appendChild(c);m(a,c)});h[0].appendChild(D);s.$render();s.$isEmpty(a)||(b=r.readValue(),(C.trackBy||t?na(a,b):a===b)||(s.$setViewValue(b),s.$render()))}var r=l[0],s=l[1],t=k.multiple,u;l=0;for(var p=h.children(),z=p.length;l<z;l++)if(""===p[l].value){u=
p.eq(l);break}var A=!!u,v=!1,y=F(f.cloneNode(!1));y.val("?");var w,C=c(k.ngOptions,h,d),D=b[0].createDocumentFragment(),E=function(){A?v&&u.removeAttr("selected"):u.remove()};t?(s.$isEmpty=function(a){return!a||0===a.length},r.writeValue=function(a){w.items.forEach(function(a){a.element.selected=!1});a&&a.forEach(function(a){if(a=w.getOptionFromViewValue(a))a.element.selected=!0})},r.readValue=function(){var a=h.val()||[],b=[];q(a,function(a){(a=w.selectValueMap[a])&&!a.disabled&&b.push(w.getViewValueFromOption(a))});
return b},C.trackBy&&d.$watchCollection(function(){if(I(s.$viewValue))return s.$viewValue.map(function(a){return C.getTrackByValue(a)})},function(){s.$render()})):(r.writeValue=function(a){var b=w.selectValueMap[h.val()],c=w.getOptionFromViewValue(a);b&&b.element.removeAttribute("selected");c?(h[0].value!==c.selectValue&&(y.remove(),E(),h[0].value=c.selectValue,c.element.selected=!0),c.element.setAttribute("selected","selected")):null===a||A?(y.remove(),A||h.prepend(u),h.val(""),v&&(u.prop("selected",
!0),u.attr("selected",!0))):(E(),h.prepend(y),h.val("?"),y.prop("selected",!0),y.attr("selected",!0))},r.readValue=function(){var a=w.selectValueMap[h.val()];return a&&!a.disabled?(E(),y.remove(),w.getViewValueFromOption(a)):null},C.trackBy&&d.$watch(function(){return C.getTrackByValue(s.$viewValue)},function(){s.$render()}));A?(u.remove(),a(u)(d),8===u[0].nodeType?(v=!1,r.registerOption=function(a,b){""===b.val()&&(v=!0,u=b,u.removeClass("ng-scope"),s.$render(),b.on("$destroy",function(){u=void 0;
v=!1}))}):(u.removeClass("ng-scope"),v=!0)):u=F(f.cloneNode(!1));h.empty();n();d.$watchCollection(C.getWatchables,n)}}}}],Ve=["$locale","$interpolate","$log",function(a,b,d){var c=/{}/g,f=/^when(Minus)?(.+)$/;return{link:function(e,g,h){function k(a){g.text(a||"")}var l=h.count,m=h.$attr.when&&g.attr(h.$attr.when),n=h.offset||0,r=e.$eval(m)||{},s={},t=b.startSymbol(),u=b.endSymbol(),p=t+l+"-"+n+u,x=$.noop,A;q(h,function(a,b){var c=f.exec(b);c&&(c=(c[1]?"-":"")+Q(c[2]),r[c]=g.attr(h.$attr[b]))});q(r,
function(a,d){s[d]=b(a.replace(c,p))});e.$watch(l,function(b){var c=parseFloat(b),f=ia(c);f||c in r||(c=a.pluralCat(c-n));c===A||f&&ia(A)||(x(),f=s[c],z(f)?(null!=b&&d.debug("ngPluralize: no rule defined for '"+c+"' in "+m),x=w,k()):x=e.$watch(f,k),A=c)})}}}],We=["$parse","$animate","$compile",function(a,b,d){var c=G("ngRepeat"),f=function(a,b,c,d,f,m,n){a[c]=d;f&&(a[f]=m);a.$index=b;a.$first=0===b;a.$last=b===n-1;a.$middle=!(a.$first||a.$last);a.$odd=!(a.$even=0===(b&1))};return{restrict:"A",multiElement:!0,
transclude:"element",priority:1E3,terminal:!0,$$tlb:!0,compile:function(e,g){var h=g.ngRepeat,k=d.$$createComment("end ngRepeat",h),l=h.match(/^\s*([\s\S]+?)\s+in\s+([\s\S]+?)(?:\s+as\s+([\s\S]+?))?(?:\s+track\s+by\s+([\s\S]+?))?\s*$/);if(!l)throw c("iexp",h);var m=l[1],n=l[2],r=l[3],s=l[4],l=m.match(/^(?:(\s*[$\w]+)|\(\s*([$\w]+)\s*,\s*([$\w]+)\s*\))$/);if(!l)throw c("iidexp",m);var t=l[3]||l[1],u=l[2];if(r&&(!/^[$a-zA-Z_][$a-zA-Z0-9_]*$/.test(r)||/^(null|undefined|this|\$index|\$first|\$middle|\$last|\$even|\$odd|\$parent|\$root|\$id)$/.test(r)))throw c("badident",
r);var p,x,A,v,w={$id:Aa};s?p=a(s):(A=function(a,b){return Aa(b)},v=function(a){return a});return function(a,d,e,g,l){p&&(x=function(b,c,d){u&&(w[u]=b);w[t]=c;w.$index=d;return p(a,w)});var m=V();a.$watchCollection(n,function(e){var g,n,p=d[0],s,w=V(),z,y,C,D,F,E,G;r&&(a[r]=e);if(la(e))F=e,n=x||A;else for(G in n=x||v,F=[],e)ua.call(e,G)&&"$"!==G.charAt(0)&&F.push(G);z=F.length;G=Array(z);for(g=0;g<z;g++)if(y=e===F?g:F[g],C=e[y],D=n(y,C,g),m[D])E=m[D],delete m[D],w[D]=E,G[g]=E;else{if(w[D])throw q(G,
function(a){a&&a.scope&&(m[a.id]=a)}),c("dupes",h,D,C);G[g]={id:D,scope:void 0,clone:void 0};w[D]=!0}for(s in m){E=m[s];D=vb(E.clone);b.leave(D);if(D[0].parentNode)for(g=0,n=D.length;g<n;g++)D[g].$$NG_REMOVED=!0;E.scope.$destroy()}for(g=0;g<z;g++)if(y=e===F?g:F[g],C=e[y],E=G[g],E.scope){s=p;do s=s.nextSibling;while(s&&s.$$NG_REMOVED);E.clone[0]!==s&&b.move(vb(E.clone),null,p);p=E.clone[E.clone.length-1];f(E.scope,g,t,C,u,y,z)}else l(function(a,c){E.scope=c;var d=k.cloneNode(!1);a[a.length++]=d;b.enter(a,
null,p);p=d;E.clone=a;w[E.id]=E;f(E.scope,g,t,C,u,y,z)});m=w})}}}}],Xe=["$animate",function(a){return{restrict:"A",multiElement:!0,link:function(b,d,c){b.$watch(c.ngShow,function(b){a[b?"removeClass":"addClass"](d,"ng-hide",{tempClasses:"ng-hide-animate"})})}}}],Qe=["$animate",function(a){return{restrict:"A",multiElement:!0,link:function(b,d,c){b.$watch(c.ngHide,function(b){a[b?"addClass":"removeClass"](d,"ng-hide",{tempClasses:"ng-hide-animate"})})}}}],Ye=Va(function(a,b,d){a.$watch(d.ngStyle,function(a,
d){d&&a!==d&&q(d,function(a,c){b.css(c,"")});a&&b.css(a)},!0)}),Ze=["$animate","$compile",function(a,b){return{require:"ngSwitch",controller:["$scope",function(){this.cases={}}],link:function(d,c,f,e){var g=[],h=[],k=[],l=[],m=function(a,b){return function(c){!1!==c&&a.splice(b,1)}};d.$watch(f.ngSwitch||f.on,function(c){for(var d,f;k.length;)a.cancel(k.pop());d=0;for(f=l.length;d<f;++d){var t=vb(h[d].clone);l[d].$destroy();(k[d]=a.leave(t)).done(m(k,d))}h.length=0;l.length=0;(g=e.cases["!"+c]||e.cases["?"])&&
q(g,function(c){c.transclude(function(d,e){l.push(e);var f=c.element;d[d.length++]=b.$$createComment("end ngSwitchWhen");h.push({clone:d});a.enter(d,f.parent(),f)})})})}}}],$e=Va({transclude:"element",priority:1200,require:"^ngSwitch",multiElement:!0,link:function(a,b,d,c,f){a=d.ngSwitchWhen.split(d.ngSwitchWhenSeparator).sort().filter(function(a,b,c){return c[b-1]!==a});q(a,function(a){c.cases["!"+a]=c.cases["!"+a]||[];c.cases["!"+a].push({transclude:f,element:b})})}}),af=Va({transclude:"element",
priority:1200,require:"^ngSwitch",multiElement:!0,link:function(a,b,d,c,f){c.cases["?"]=c.cases["?"]||[];c.cases["?"].push({transclude:f,element:b})}}),kh=G("ngTransclude"),cf=["$compile",function(a){return{restrict:"EAC",terminal:!0,compile:function(b){var d=a(b.contents());b.empty();return function(a,b,e,g,h){function k(){d(a,function(a){b.append(a)})}if(!h)throw kh("orphan",ya(b));e.ngTransclude===e.$attr.ngTransclude&&(e.ngTransclude="");e=e.ngTransclude||e.ngTranscludeSlot;h(function(a,c){a.length?
b.append(a):(k(),c.$destroy())},null,e);e&&!h.isSlotFilled(e)&&k()}}}}],Ee=["$templateCache",function(a){return{restrict:"E",terminal:!0,compile:function(b,d){"text/ng-template"===d.type&&a.put(d.id,b[0].text)}}}],lh={$setViewValue:w,$render:w},mh=["$element","$scope",function(a,b){var d=this,c=new Sa;d.ngModelCtrl=lh;d.unknownOption=F(y.document.createElement("option"));d.renderUnknownOption=function(b){b="? "+Aa(b)+" ?";d.unknownOption.val(b);a.prepend(d.unknownOption);a.val(b)};b.$on("$destroy",
function(){d.renderUnknownOption=w});d.removeUnknownOption=function(){d.unknownOption.parent()&&d.unknownOption.remove()};d.readValue=function(){d.removeUnknownOption();return a.val()};d.writeValue=function(b){d.hasOption(b)?(d.removeUnknownOption(),a.val(b),""===b&&d.emptyOption.prop("selected",!0)):null==b&&d.emptyOption?(d.removeUnknownOption(),a.val("")):d.renderUnknownOption(b)};d.addOption=function(a,b){if(8!==b[0].nodeType){Ra(a,'"option value"');""===a&&(d.emptyOption=b);var g=c.get(a)||0;
c.put(a,g+1);d.ngModelCtrl.$render();b[0].hasAttribute("selected")&&(b[0].selected=!0)}};d.removeOption=function(a){var b=c.get(a);b&&(1===b?(c.remove(a),""===a&&(d.emptyOption=void 0)):c.put(a,b-1))};d.hasOption=function(a){return!!c.get(a)};d.registerOption=function(a,b,c,h,k){if(h){var l;c.$observe("value",function(a){x(l)&&d.removeOption(l);l=a;d.addOption(a,b)})}else k?a.$watch(k,function(a,f){c.$set("value",a);f!==a&&d.removeOption(f);d.addOption(a,b)}):d.addOption(c.value,b);b.on("$destroy",
function(){d.removeOption(c.value);d.ngModelCtrl.$render()})}}],Fe=function(){return{restrict:"E",require:["select","?ngModel"],controller:mh,priority:1,link:{pre:function(a,b,d,c){var f=c[1];if(f){var e=c[0];e.ngModelCtrl=f;b.on("change",function(){a.$apply(function(){f.$setViewValue(e.readValue())})});if(d.multiple){e.readValue=function(){var a=[];q(b.find("option"),function(b){b.selected&&a.push(b.value)});return a};e.writeValue=function(a){var c=new Sa(a);q(b.find("option"),function(a){a.selected=
x(c.get(a.value))})};var g,h=NaN;a.$watch(function(){h!==f.$viewValue||na(g,f.$viewValue)||(g=ka(f.$viewValue),f.$render());h=f.$viewValue});f.$isEmpty=function(a){return!a||0===a.length}}}},post:function(a,b,d,c){var f=c[1];if(f){var e=c[0];f.$render=function(){e.writeValue(f.$viewValue)}}}}}},Ge=["$interpolate",function(a){return{restrict:"E",priority:100,compile:function(b,d){var c,f;x(d.ngValue)?c=!0:x(d.value)?c=a(d.value,!0):(f=a(b.text(),!0))||d.$set("value",b.text());return function(a,b,d){var k=
b.parent();(k=k.data("$selectController")||k.parent().data("$selectController"))&&k.registerOption(a,b,d,c,f)}}}}],Nc=function(){return{restrict:"A",require:"?ngModel",link:function(a,b,d,c){c&&(d.required=!0,c.$validators.required=function(a,b){return!d.required||!c.$isEmpty(b)},d.$observe("required",function(){c.$validate()}))}}},Mc=function(){return{restrict:"A",require:"?ngModel",link:function(a,b,d,c){if(c){var f,e=d.ngPattern||d.pattern;d.$observe("pattern",function(a){D(a)&&0<a.length&&(a=
new RegExp("^"+a+"$"));if(a&&!a.test)throw G("ngPattern")("noregexp",e,a,ya(b));f=a||void 0;c.$validate()});c.$validators.pattern=function(a,b){return c.$isEmpty(b)||z(f)||f.test(b)}}}}},Pc=function(){return{restrict:"A",require:"?ngModel",link:function(a,b,d,c){if(c){var f=-1;d.$observe("maxlength",function(a){a=Z(a);f=ia(a)?-1:a;c.$validate()});c.$validators.maxlength=function(a,b){return 0>f||c.$isEmpty(b)||b.length<=f}}}}},Oc=function(){return{restrict:"A",require:"?ngModel",link:function(a,b,
d,c){if(c){var f=0;d.$observe("minlength",function(a){f=Z(a)||0;c.$validate()});c.$validators.minlength=function(a,b){return c.$isEmpty(b)||b.length>=f}}}}};y.angular.bootstrap?y.console&&console.log("WARNING: Tried to load angular more than once."):(xe(),ze($),$.module("ngLocale",[],["$provide",function(a){function b(a){a+="";var b=a.indexOf(".");return-1==b?0:a.length-b-1}a.value("$locale",{DATETIME_FORMATS:{AMPMS:["AM","PM"],DAY:"Sunday Monday Tuesday Wednesday Thursday Friday Saturday".split(" "),
ERANAMES:["Before Christ","Anno Domini"],ERAS:["BC","AD"],FIRSTDAYOFWEEK:6,MONTH:"January February March April May June July August September October November December".split(" "),SHORTDAY:"Sun Mon Tue Wed Thu Fri Sat".split(" "),SHORTMONTH:"Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(" "),STANDALONEMONTH:"January February March April May June July August September October November December".split(" "),WEEKENDRANGE:[5,6],fullDate:"EEEE, MMMM d, y",longDate:"MMMM d, y",medium:"MMM d, y h:mm:ss a",
mediumDate:"MMM d, y",mediumTime:"h:mm:ss a","short":"M/d/yy h:mm a",shortDate:"M/d/yy",shortTime:"h:mm a"},NUMBER_FORMATS:{CURRENCY_SYM:"$",DECIMAL_SEP:".",GROUP_SEP:",",PATTERNS:[{gSize:3,lgSize:3,maxFrac:3,minFrac:0,minInt:1,negPre:"-",negSuf:"",posPre:"",posSuf:""},{gSize:3,lgSize:3,maxFrac:2,minFrac:2,minInt:1,negPre:"-\u00a4",negSuf:"",posPre:"\u00a4",posSuf:""}]},id:"en-us",localeID:"en_US",pluralCat:function(a,c){var f=a|0,e=c;void 0===e&&(e=Math.min(b(a),3));Math.pow(10,e);return 1==f&&0==
e?"one":"other"}})}]),F(y.document).ready(function(){se(y.document,Gc)}))})(window);!window.angular.$$csp().noInlineStyle&&window.angular.element(document.head).prepend('<style type="text/css">@charset "UTF-8";[ng\\:cloak],[ng-cloak],[data-ng-cloak],[x-ng-cloak],.ng-cloak,.x-ng-cloak,.ng-hide:not(.ng-hide-animate){display:none !important;}ng\\:form{display:block;}.ng-animate-shim{visibility:hidden;}.ng-anchor{position:absolute;}</style>');
//# sourceMappingURL=angular.min.js.map
;/**
 * @license AngularJS v1.5.8
 * (c) 2010-2016 Google, Inc. http://angularjs.org
 * License: MIT
 */
(function(window, angular) {

'use strict';

/**
 * @ngdoc object
 * @name angular.mock
 * @description
 *
 * Namespace from 'angular-mocks.js' which contains testing related code.
 *
 */
angular.mock = {};

/**
 * ! This is a private undocumented service !
 *
 * @name $browser
 *
 * @description
 * This service is a mock implementation of {@link ng.$browser}. It provides fake
 * implementation for commonly used browser apis that are hard to test, e.g. setTimeout, xhr,
 * cookies, etc.
 *
 * The api of this service is the same as that of the real {@link ng.$browser $browser}, except
 * that there are several helper methods available which can be used in tests.
 */
angular.mock.$BrowserProvider = function() {
  this.$get = function() {
    return new angular.mock.$Browser();
  };
};

angular.mock.$Browser = function() {
  var self = this;

  this.isMock = true;
  self.$$url = "http://server/";
  self.$$lastUrl = self.$$url; // used by url polling fn
  self.pollFns = [];

  // TODO(vojta): remove this temporary api
  self.$$completeOutstandingRequest = angular.noop;
  self.$$incOutstandingRequestCount = angular.noop;


  // register url polling fn

  self.onUrlChange = function(listener) {
    self.pollFns.push(
      function() {
        if (self.$$lastUrl !== self.$$url || self.$$state !== self.$$lastState) {
          self.$$lastUrl = self.$$url;
          self.$$lastState = self.$$state;
          listener(self.$$url, self.$$state);
        }
      }
    );

    return listener;
  };

  self.$$applicationDestroyed = angular.noop;
  self.$$checkUrlChange = angular.noop;

  self.deferredFns = [];
  self.deferredNextId = 0;

  self.defer = function(fn, delay) {
    delay = delay || 0;
    self.deferredFns.push({time:(self.defer.now + delay), fn:fn, id: self.deferredNextId});
    self.deferredFns.sort(function(a, b) { return a.time - b.time;});
    return self.deferredNextId++;
  };


  /**
   * @name $browser#defer.now
   *
   * @description
   * Current milliseconds mock time.
   */
  self.defer.now = 0;


  self.defer.cancel = function(deferId) {
    var fnIndex;

    angular.forEach(self.deferredFns, function(fn, index) {
      if (fn.id === deferId) fnIndex = index;
    });

    if (angular.isDefined(fnIndex)) {
      self.deferredFns.splice(fnIndex, 1);
      return true;
    }

    return false;
  };


  /**
   * @name $browser#defer.flush
   *
   * @description
   * Flushes all pending requests and executes the defer callbacks.
   *
   * @param {number=} number of milliseconds to flush. See {@link #defer.now}
   */
  self.defer.flush = function(delay) {
    var nextTime;

    if (angular.isDefined(delay)) {
      // A delay was passed so compute the next time
      nextTime = self.defer.now + delay;
    } else {
      if (self.deferredFns.length) {
        // No delay was passed so set the next time so that it clears the deferred queue
        nextTime = self.deferredFns[self.deferredFns.length - 1].time;
      } else {
        // No delay passed, but there are no deferred tasks so flush - indicates an error!
        throw new Error('No deferred tasks to be flushed');
      }
    }

    while (self.deferredFns.length && self.deferredFns[0].time <= nextTime) {
      // Increment the time and call the next deferred function
      self.defer.now = self.deferredFns[0].time;
      self.deferredFns.shift().fn();
    }

    // Ensure that the current time is correct
    self.defer.now = nextTime;
  };

  self.$$baseHref = '/';
  self.baseHref = function() {
    return this.$$baseHref;
  };
};
angular.mock.$Browser.prototype = {

  /**
   * @name $browser#poll
   *
   * @description
   * run all fns in pollFns
   */
  poll: function poll() {
    angular.forEach(this.pollFns, function(pollFn) {
      pollFn();
    });
  },

  url: function(url, replace, state) {
    if (angular.isUndefined(state)) {
      state = null;
    }
    if (url) {
      this.$$url = url;
      // Native pushState serializes & copies the object; simulate it.
      this.$$state = angular.copy(state);
      return this;
    }

    return this.$$url;
  },

  state: function() {
    return this.$$state;
  },

  notifyWhenNoOutstandingRequests: function(fn) {
    fn();
  }
};


/**
 * @ngdoc provider
 * @name $exceptionHandlerProvider
 *
 * @description
 * Configures the mock implementation of {@link ng.$exceptionHandler} to rethrow or to log errors
 * passed to the `$exceptionHandler`.
 */

/**
 * @ngdoc service
 * @name $exceptionHandler
 *
 * @description
 * Mock implementation of {@link ng.$exceptionHandler} that rethrows or logs errors passed
 * to it. See {@link ngMock.$exceptionHandlerProvider $exceptionHandlerProvider} for configuration
 * information.
 *
 *
 * ```js
 *   describe('$exceptionHandlerProvider', function() {
 *
 *     it('should capture log messages and exceptions', function() {
 *
 *       module(function($exceptionHandlerProvider) {
 *         $exceptionHandlerProvider.mode('log');
 *       });
 *
 *       inject(function($log, $exceptionHandler, $timeout) {
 *         $timeout(function() { $log.log(1); });
 *         $timeout(function() { $log.log(2); throw 'banana peel'; });
 *         $timeout(function() { $log.log(3); });
 *         expect($exceptionHandler.errors).toEqual([]);
 *         expect($log.assertEmpty());
 *         $timeout.flush();
 *         expect($exceptionHandler.errors).toEqual(['banana peel']);
 *         expect($log.log.logs).toEqual([[1], [2], [3]]);
 *       });
 *     });
 *   });
 * ```
 */

angular.mock.$ExceptionHandlerProvider = function() {
  var handler;

  /**
   * @ngdoc method
   * @name $exceptionHandlerProvider#mode
   *
   * @description
   * Sets the logging mode.
   *
   * @param {string} mode Mode of operation, defaults to `rethrow`.
   *
   *   - `log`: Sometimes it is desirable to test that an error is thrown, for this case the `log`
   *     mode stores an array of errors in `$exceptionHandler.errors`, to allow later assertion of
   *     them. See {@link ngMock.$log#assertEmpty assertEmpty()} and
   *     {@link ngMock.$log#reset reset()}.
   *   - `rethrow`: If any errors are passed to the handler in tests, it typically means that there
   *     is a bug in the application or test, so this mock will make these tests fail. For any
   *     implementations that expect exceptions to be thrown, the `rethrow` mode will also maintain
   *     a log of thrown errors in `$exceptionHandler.errors`.
   */
  this.mode = function(mode) {

    switch (mode) {
      case 'log':
      case 'rethrow':
        var errors = [];
        handler = function(e) {
          if (arguments.length == 1) {
            errors.push(e);
          } else {
            errors.push([].slice.call(arguments, 0));
          }
          if (mode === "rethrow") {
            throw e;
          }
        };
        handler.errors = errors;
        break;
      default:
        throw new Error("Unknown mode '" + mode + "', only 'log'/'rethrow' modes are allowed!");
    }
  };

  this.$get = function() {
    return handler;
  };

  this.mode('rethrow');
};


/**
 * @ngdoc service
 * @name $log
 *
 * @description
 * Mock implementation of {@link ng.$log} that gathers all logged messages in arrays
 * (one array per logging level). These arrays are exposed as `logs` property of each of the
 * level-specific log function, e.g. for level `error` the array is exposed as `$log.error.logs`.
 *
 */
angular.mock.$LogProvider = function() {
  var debug = true;

  function concat(array1, array2, index) {
    return array1.concat(Array.prototype.slice.call(array2, index));
  }

  this.debugEnabled = function(flag) {
    if (angular.isDefined(flag)) {
      debug = flag;
      return this;
    } else {
      return debug;
    }
  };

  this.$get = function() {
    var $log = {
      log: function() { $log.log.logs.push(concat([], arguments, 0)); },
      warn: function() { $log.warn.logs.push(concat([], arguments, 0)); },
      info: function() { $log.info.logs.push(concat([], arguments, 0)); },
      error: function() { $log.error.logs.push(concat([], arguments, 0)); },
      debug: function() {
        if (debug) {
          $log.debug.logs.push(concat([], arguments, 0));
        }
      }
    };

    /**
     * @ngdoc method
     * @name $log#reset
     *
     * @description
     * Reset all of the logging arrays to empty.
     */
    $log.reset = function() {
      /**
       * @ngdoc property
       * @name $log#log.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#log `log()`}.
       *
       * @example
       * ```js
       * $log.log('Some Log');
       * var first = $log.log.logs.unshift();
       * ```
       */
      $log.log.logs = [];
      /**
       * @ngdoc property
       * @name $log#info.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#info `info()`}.
       *
       * @example
       * ```js
       * $log.info('Some Info');
       * var first = $log.info.logs.unshift();
       * ```
       */
      $log.info.logs = [];
      /**
       * @ngdoc property
       * @name $log#warn.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#warn `warn()`}.
       *
       * @example
       * ```js
       * $log.warn('Some Warning');
       * var first = $log.warn.logs.unshift();
       * ```
       */
      $log.warn.logs = [];
      /**
       * @ngdoc property
       * @name $log#error.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#error `error()`}.
       *
       * @example
       * ```js
       * $log.error('Some Error');
       * var first = $log.error.logs.unshift();
       * ```
       */
      $log.error.logs = [];
        /**
       * @ngdoc property
       * @name $log#debug.logs
       *
       * @description
       * Array of messages logged using {@link ng.$log#debug `debug()`}.
       *
       * @example
       * ```js
       * $log.debug('Some Error');
       * var first = $log.debug.logs.unshift();
       * ```
       */
      $log.debug.logs = [];
    };

    /**
     * @ngdoc method
     * @name $log#assertEmpty
     *
     * @description
     * Assert that all of the logging methods have no logged messages. If any messages are present,
     * an exception is thrown.
     */
    $log.assertEmpty = function() {
      var errors = [];
      angular.forEach(['error', 'warn', 'info', 'log', 'debug'], function(logLevel) {
        angular.forEach($log[logLevel].logs, function(log) {
          angular.forEach(log, function(logItem) {
            errors.push('MOCK $log (' + logLevel + '): ' + String(logItem) + '\n' +
                        (logItem.stack || ''));
          });
        });
      });
      if (errors.length) {
        errors.unshift("Expected $log to be empty! Either a message was logged unexpectedly, or " +
          "an expected log message was not checked and removed:");
        errors.push('');
        throw new Error(errors.join('\n---------\n'));
      }
    };

    $log.reset();
    return $log;
  };
};


/**
 * @ngdoc service
 * @name $interval
 *
 * @description
 * Mock implementation of the $interval service.
 *
 * Use {@link ngMock.$interval#flush `$interval.flush(millis)`} to
 * move forward by `millis` milliseconds and trigger any functions scheduled to run in that
 * time.
 *
 * @param {function()} fn A function that should be called repeatedly.
 * @param {number} delay Number of milliseconds between each function call.
 * @param {number=} [count=0] Number of times to repeat. If not set, or 0, will repeat
 *   indefinitely.
 * @param {boolean=} [invokeApply=true] If set to `false` skips model dirty checking, otherwise
 *   will invoke `fn` within the {@link ng.$rootScope.Scope#$apply $apply} block.
 * @param {...*=} Pass additional parameters to the executed function.
 * @returns {promise} A promise which will be notified on each iteration.
 */
angular.mock.$IntervalProvider = function() {
  this.$get = ['$browser', '$rootScope', '$q', '$$q',
       function($browser,   $rootScope,   $q,   $$q) {
    var repeatFns = [],
        nextRepeatId = 0,
        now = 0;

    var $interval = function(fn, delay, count, invokeApply) {
      var hasParams = arguments.length > 4,
          args = hasParams ? Array.prototype.slice.call(arguments, 4) : [],
          iteration = 0,
          skipApply = (angular.isDefined(invokeApply) && !invokeApply),
          deferred = (skipApply ? $$q : $q).defer(),
          promise = deferred.promise;

      count = (angular.isDefined(count)) ? count : 0;
      promise.then(null, null, (!hasParams) ? fn : function() {
        fn.apply(null, args);
      });

      promise.$$intervalId = nextRepeatId;

      function tick() {
        deferred.notify(iteration++);

        if (count > 0 && iteration >= count) {
          var fnIndex;
          deferred.resolve(iteration);

          angular.forEach(repeatFns, function(fn, index) {
            if (fn.id === promise.$$intervalId) fnIndex = index;
          });

          if (angular.isDefined(fnIndex)) {
            repeatFns.splice(fnIndex, 1);
          }
        }

        if (skipApply) {
          $browser.defer.flush();
        } else {
          $rootScope.$apply();
        }
      }

      repeatFns.push({
        nextTime:(now + delay),
        delay: delay,
        fn: tick,
        id: nextRepeatId,
        deferred: deferred
      });
      repeatFns.sort(function(a, b) { return a.nextTime - b.nextTime;});

      nextRepeatId++;
      return promise;
    };
    /**
     * @ngdoc method
     * @name $interval#cancel
     *
     * @description
     * Cancels a task associated with the `promise`.
     *
     * @param {promise} promise A promise from calling the `$interval` function.
     * @returns {boolean} Returns `true` if the task was successfully cancelled.
     */
    $interval.cancel = function(promise) {
      if (!promise) return false;
      var fnIndex;

      angular.forEach(repeatFns, function(fn, index) {
        if (fn.id === promise.$$intervalId) fnIndex = index;
      });

      if (angular.isDefined(fnIndex)) {
        repeatFns[fnIndex].deferred.reject('canceled');
        repeatFns.splice(fnIndex, 1);
        return true;
      }

      return false;
    };

    /**
     * @ngdoc method
     * @name $interval#flush
     * @description
     *
     * Runs interval tasks scheduled to be run in the next `millis` milliseconds.
     *
     * @param {number=} millis maximum timeout amount to flush up until.
     *
     * @return {number} The amount of time moved forward.
     */
    $interval.flush = function(millis) {
      now += millis;
      while (repeatFns.length && repeatFns[0].nextTime <= now) {
        var task = repeatFns[0];
        task.fn();
        task.nextTime += task.delay;
        repeatFns.sort(function(a, b) { return a.nextTime - b.nextTime;});
      }
      return millis;
    };

    return $interval;
  }];
};


/* jshint -W101 */
/* The R_ISO8061_STR regex is never going to fit into the 100 char limit!
 * This directive should go inside the anonymous function but a bug in JSHint means that it would
 * not be enacted early enough to prevent the warning.
 */
var R_ISO8061_STR = /^(-?\d{4})-?(\d\d)-?(\d\d)(?:T(\d\d)(?:\:?(\d\d)(?:\:?(\d\d)(?:\.(\d{3}))?)?)?(Z|([+-])(\d\d):?(\d\d)))?$/;

function jsonStringToDate(string) {
  var match;
  if (match = string.match(R_ISO8061_STR)) {
    var date = new Date(0),
        tzHour = 0,
        tzMin  = 0;
    if (match[9]) {
      tzHour = toInt(match[9] + match[10]);
      tzMin = toInt(match[9] + match[11]);
    }
    date.setUTCFullYear(toInt(match[1]), toInt(match[2]) - 1, toInt(match[3]));
    date.setUTCHours(toInt(match[4] || 0) - tzHour,
                     toInt(match[5] || 0) - tzMin,
                     toInt(match[6] || 0),
                     toInt(match[7] || 0));
    return date;
  }
  return string;
}

function toInt(str) {
  return parseInt(str, 10);
}

function padNumberInMock(num, digits, trim) {
  var neg = '';
  if (num < 0) {
    neg =  '-';
    num = -num;
  }
  num = '' + num;
  while (num.length < digits) num = '0' + num;
  if (trim) {
    num = num.substr(num.length - digits);
  }
  return neg + num;
}


/**
 * @ngdoc type
 * @name angular.mock.TzDate
 * @description
 *
 * *NOTE*: this is not an injectable instance, just a globally available mock class of `Date`.
 *
 * Mock of the Date type which has its timezone specified via constructor arg.
 *
 * The main purpose is to create Date-like instances with timezone fixed to the specified timezone
 * offset, so that we can test code that depends on local timezone settings without dependency on
 * the time zone settings of the machine where the code is running.
 *
 * @param {number} offset Offset of the *desired* timezone in hours (fractions will be honored)
 * @param {(number|string)} timestamp Timestamp representing the desired time in *UTC*
 *
 * @example
 * !!!! WARNING !!!!!
 * This is not a complete Date object so only methods that were implemented can be called safely.
 * To make matters worse, TzDate instances inherit stuff from Date via a prototype.
 *
 * We do our best to intercept calls to "unimplemented" methods, but since the list of methods is
 * incomplete we might be missing some non-standard methods. This can result in errors like:
 * "Date.prototype.foo called on incompatible Object".
 *
 * ```js
 * var newYearInBratislava = new TzDate(-1, '2009-12-31T23:00:00Z');
 * newYearInBratislava.getTimezoneOffset() => -60;
 * newYearInBratislava.getFullYear() => 2010;
 * newYearInBratislava.getMonth() => 0;
 * newYearInBratislava.getDate() => 1;
 * newYearInBratislava.getHours() => 0;
 * newYearInBratislava.getMinutes() => 0;
 * newYearInBratislava.getSeconds() => 0;
 * ```
 *
 */
angular.mock.TzDate = function(offset, timestamp) {
  var self = new Date(0);
  if (angular.isString(timestamp)) {
    var tsStr = timestamp;

    self.origDate = jsonStringToDate(timestamp);

    timestamp = self.origDate.getTime();
    if (isNaN(timestamp)) {
      throw {
        name: "Illegal Argument",
        message: "Arg '" + tsStr + "' passed into TzDate constructor is not a valid date string"
      };
    }
  } else {
    self.origDate = new Date(timestamp);
  }

  var localOffset = new Date(timestamp).getTimezoneOffset();
  self.offsetDiff = localOffset * 60 * 1000 - offset * 1000 * 60 * 60;
  self.date = new Date(timestamp + self.offsetDiff);

  self.getTime = function() {
    return self.date.getTime() - self.offsetDiff;
  };

  self.toLocaleDateString = function() {
    return self.date.toLocaleDateString();
  };

  self.getFullYear = function() {
    return self.date.getFullYear();
  };

  self.getMonth = function() {
    return self.date.getMonth();
  };

  self.getDate = function() {
    return self.date.getDate();
  };

  self.getHours = function() {
    return self.date.getHours();
  };

  self.getMinutes = function() {
    return self.date.getMinutes();
  };

  self.getSeconds = function() {
    return self.date.getSeconds();
  };

  self.getMilliseconds = function() {
    return self.date.getMilliseconds();
  };

  self.getTimezoneOffset = function() {
    return offset * 60;
  };

  self.getUTCFullYear = function() {
    return self.origDate.getUTCFullYear();
  };

  self.getUTCMonth = function() {
    return self.origDate.getUTCMonth();
  };

  self.getUTCDate = function() {
    return self.origDate.getUTCDate();
  };

  self.getUTCHours = function() {
    return self.origDate.getUTCHours();
  };

  self.getUTCMinutes = function() {
    return self.origDate.getUTCMinutes();
  };

  self.getUTCSeconds = function() {
    return self.origDate.getUTCSeconds();
  };

  self.getUTCMilliseconds = function() {
    return self.origDate.getUTCMilliseconds();
  };

  self.getDay = function() {
    return self.date.getDay();
  };

  // provide this method only on browsers that already have it
  if (self.toISOString) {
    self.toISOString = function() {
      return padNumberInMock(self.origDate.getUTCFullYear(), 4) + '-' +
            padNumberInMock(self.origDate.getUTCMonth() + 1, 2) + '-' +
            padNumberInMock(self.origDate.getUTCDate(), 2) + 'T' +
            padNumberInMock(self.origDate.getUTCHours(), 2) + ':' +
            padNumberInMock(self.origDate.getUTCMinutes(), 2) + ':' +
            padNumberInMock(self.origDate.getUTCSeconds(), 2) + '.' +
            padNumberInMock(self.origDate.getUTCMilliseconds(), 3) + 'Z';
    };
  }

  //hide all methods not implemented in this mock that the Date prototype exposes
  var unimplementedMethods = ['getUTCDay',
      'getYear', 'setDate', 'setFullYear', 'setHours', 'setMilliseconds',
      'setMinutes', 'setMonth', 'setSeconds', 'setTime', 'setUTCDate', 'setUTCFullYear',
      'setUTCHours', 'setUTCMilliseconds', 'setUTCMinutes', 'setUTCMonth', 'setUTCSeconds',
      'setYear', 'toDateString', 'toGMTString', 'toJSON', 'toLocaleFormat', 'toLocaleString',
      'toLocaleTimeString', 'toSource', 'toString', 'toTimeString', 'toUTCString', 'valueOf'];

  angular.forEach(unimplementedMethods, function(methodName) {
    self[methodName] = function() {
      throw new Error("Method '" + methodName + "' is not implemented in the TzDate mock");
    };
  });

  return self;
};

//make "tzDateInstance instanceof Date" return true
angular.mock.TzDate.prototype = Date.prototype;
/* jshint +W101 */


/**
 * @ngdoc service
 * @name $animate
 *
 * @description
 * Mock implementation of the {@link ng.$animate `$animate`} service. Exposes two additional methods
 * for testing animations.
 *
 * You need to require the `ngAnimateMock` module in your test suite for instance `beforeEach(module('ngAnimateMock'))`
 */
angular.mock.animate = angular.module('ngAnimateMock', ['ng'])

  .config(['$provide', function($provide) {

    $provide.factory('$$forceReflow', function() {
      function reflowFn() {
        reflowFn.totalReflows++;
      }
      reflowFn.totalReflows = 0;
      return reflowFn;
    });

    $provide.factory('$$animateAsyncRun', function() {
      var queue = [];
      var queueFn = function() {
        return function(fn) {
          queue.push(fn);
        };
      };
      queueFn.flush = function() {
        if (queue.length === 0) return false;

        for (var i = 0; i < queue.length; i++) {
          queue[i]();
        }
        queue = [];

        return true;
      };
      return queueFn;
    });

    $provide.decorator('$$animateJs', ['$delegate', function($delegate) {
      var runners = [];

      var animateJsConstructor = function() {
        var animator = $delegate.apply($delegate, arguments);
        // If no javascript animation is found, animator is undefined
        if (animator) {
          runners.push(animator);
        }
        return animator;
      };

      animateJsConstructor.$closeAndFlush = function() {
        runners.forEach(function(runner) {
          runner.end();
        });
        runners = [];
      };

      return animateJsConstructor;
    }]);

    $provide.decorator('$animateCss', ['$delegate', function($delegate) {
      var runners = [];

      var animateCssConstructor = function(element, options) {
        var animator = $delegate(element, options);
        runners.push(animator);
        return animator;
      };

      animateCssConstructor.$closeAndFlush = function() {
        runners.forEach(function(runner) {
          runner.end();
        });
        runners = [];
      };

      return animateCssConstructor;
    }]);

    $provide.decorator('$animate', ['$delegate', '$timeout', '$browser', '$$rAF', '$animateCss', '$$animateJs',
                                    '$$forceReflow', '$$animateAsyncRun', '$rootScope',
                            function($delegate,   $timeout,   $browser,   $$rAF,   $animateCss,   $$animateJs,
                                     $$forceReflow,   $$animateAsyncRun,  $rootScope) {
      var animate = {
        queue: [],
        cancel: $delegate.cancel,
        on: $delegate.on,
        off: $delegate.off,
        pin: $delegate.pin,
        get reflows() {
          return $$forceReflow.totalReflows;
        },
        enabled: $delegate.enabled,
        /**
         * @ngdoc method
         * @name $animate#closeAndFlush
         * @description
         *
         * This method will close all pending animations (both {@link ngAnimate#javascript-based-animations Javascript}
         * and {@link ngAnimate.$animateCss CSS}) and it will also flush any remaining animation frames and/or callbacks.
         */
        closeAndFlush: function() {
          // we allow the flush command to swallow the errors
          // because depending on whether CSS or JS animations are
          // used, there may not be a RAF flush. The primary flush
          // at the end of this function must throw an exception
          // because it will track if there were pending animations
          this.flush(true);
          $animateCss.$closeAndFlush();
          $$animateJs.$closeAndFlush();
          this.flush();
        },
        /**
         * @ngdoc method
         * @name $animate#flush
         * @description
         *
         * This method is used to flush the pending callbacks and animation frames to either start
         * an animation or conclude an animation. Note that this will not actually close an
         * actively running animation (see {@link ngMock.$animate#closeAndFlush `closeAndFlush()`} for that).
         */
        flush: function(hideErrors) {
          $rootScope.$digest();

          var doNextRun, somethingFlushed = false;
          do {
            doNextRun = false;

            if ($$rAF.queue.length) {
              $$rAF.flush();
              doNextRun = somethingFlushed = true;
            }

            if ($$animateAsyncRun.flush()) {
              doNextRun = somethingFlushed = true;
            }
          } while (doNextRun);

          if (!somethingFlushed && !hideErrors) {
            throw new Error('No pending animations ready to be closed or flushed');
          }

          $rootScope.$digest();
        }
      };

      angular.forEach(
        ['animate','enter','leave','move','addClass','removeClass','setClass'], function(method) {
        animate[method] = function() {
          animate.queue.push({
            event: method,
            element: arguments[0],
            options: arguments[arguments.length - 1],
            args: arguments
          });
          return $delegate[method].apply($delegate, arguments);
        };
      });

      return animate;
    }]);

  }]);


/**
 * @ngdoc function
 * @name angular.mock.dump
 * @description
 *
 * *NOTE*: This is not an injectable instance, just a globally available function.
 *
 * Method for serializing common angular objects (scope, elements, etc..) into strings.
 * It is useful for logging objects to the console when debugging.
 *
 * @param {*} object - any object to turn into string.
 * @return {string} a serialized string of the argument
 */
angular.mock.dump = function(object) {
  return serialize(object);

  function serialize(object) {
    var out;

    if (angular.isElement(object)) {
      object = angular.element(object);
      out = angular.element('<div></div>');
      angular.forEach(object, function(element) {
        out.append(angular.element(element).clone());
      });
      out = out.html();
    } else if (angular.isArray(object)) {
      out = [];
      angular.forEach(object, function(o) {
        out.push(serialize(o));
      });
      out = '[ ' + out.join(', ') + ' ]';
    } else if (angular.isObject(object)) {
      if (angular.isFunction(object.$eval) && angular.isFunction(object.$apply)) {
        out = serializeScope(object);
      } else if (object instanceof Error) {
        out = object.stack || ('' + object.name + ': ' + object.message);
      } else {
        // TODO(i): this prevents methods being logged,
        // we should have a better way to serialize objects
        out = angular.toJson(object, true);
      }
    } else {
      out = String(object);
    }

    return out;
  }

  function serializeScope(scope, offset) {
    offset = offset ||  '  ';
    var log = [offset + 'Scope(' + scope.$id + '): {'];
    for (var key in scope) {
      if (Object.prototype.hasOwnProperty.call(scope, key) && !key.match(/^(\$|this)/)) {
        log.push('  ' + key + ': ' + angular.toJson(scope[key]));
      }
    }
    var child = scope.$$childHead;
    while (child) {
      log.push(serializeScope(child, offset + '  '));
      child = child.$$nextSibling;
    }
    log.push('}');
    return log.join('\n' + offset);
  }
};

/**
 * @ngdoc service
 * @name $httpBackend
 * @description
 * Fake HTTP backend implementation suitable for unit testing applications that use the
 * {@link ng.$http $http service}.
 *
 * <div class="alert alert-info">
 * **Note**: For fake HTTP backend implementation suitable for end-to-end testing or backend-less
 * development please see {@link ngMockE2E.$httpBackend e2e $httpBackend mock}.
 * </div>
 *
 * During unit testing, we want our unit tests to run quickly and have no external dependencies so
 * we don’t want to send [XHR](https://developer.mozilla.org/en/xmlhttprequest) or
 * [JSONP](http://en.wikipedia.org/wiki/JSONP) requests to a real server. All we really need is
 * to verify whether a certain request has been sent or not, or alternatively just let the
 * application make requests, respond with pre-trained responses and assert that the end result is
 * what we expect it to be.
 *
 * This mock implementation can be used to respond with static or dynamic responses via the
 * `expect` and `when` apis and their shortcuts (`expectGET`, `whenPOST`, etc).
 *
 * When an Angular application needs some data from a server, it calls the $http service, which
 * sends the request to a real server using $httpBackend service. With dependency injection, it is
 * easy to inject $httpBackend mock (which has the same API as $httpBackend) and use it to verify
 * the requests and respond with some testing data without sending a request to a real server.
 *
 * There are two ways to specify what test data should be returned as http responses by the mock
 * backend when the code under test makes http requests:
 *
 * - `$httpBackend.expect` - specifies a request expectation
 * - `$httpBackend.when` - specifies a backend definition
 *
 *
 * ## Request Expectations vs Backend Definitions
 *
 * Request expectations provide a way to make assertions about requests made by the application and
 * to define responses for those requests. The test will fail if the expected requests are not made
 * or they are made in the wrong order.
 *
 * Backend definitions allow you to define a fake backend for your application which doesn't assert
 * if a particular request was made or not, it just returns a trained response if a request is made.
 * The test will pass whether or not the request gets made during testing.
 *
 *
 * <table class="table">
 *   <tr><th width="220px"></th><th>Request expectations</th><th>Backend definitions</th></tr>
 *   <tr>
 *     <th>Syntax</th>
 *     <td>.expect(...).respond(...)</td>
 *     <td>.when(...).respond(...)</td>
 *   </tr>
 *   <tr>
 *     <th>Typical usage</th>
 *     <td>strict unit tests</td>
 *     <td>loose (black-box) unit testing</td>
 *   </tr>
 *   <tr>
 *     <th>Fulfills multiple requests</th>
 *     <td>NO</td>
 *     <td>YES</td>
 *   </tr>
 *   <tr>
 *     <th>Order of requests matters</th>
 *     <td>YES</td>
 *     <td>NO</td>
 *   </tr>
 *   <tr>
 *     <th>Request required</th>
 *     <td>YES</td>
 *     <td>NO</td>
 *   </tr>
 *   <tr>
 *     <th>Response required</th>
 *     <td>optional (see below)</td>
 *     <td>YES</td>
 *   </tr>
 * </table>
 *
 * In cases where both backend definitions and request expectations are specified during unit
 * testing, the request expectations are evaluated first.
 *
 * If a request expectation has no response specified, the algorithm will search your backend
 * definitions for an appropriate response.
 *
 * If a request didn't match any expectation or if the expectation doesn't have the response
 * defined, the backend definitions are evaluated in sequential order to see if any of them match
 * the request. The response from the first matched definition is returned.
 *
 *
 * ## Flushing HTTP requests
 *
 * The $httpBackend used in production always responds to requests asynchronously. If we preserved
 * this behavior in unit testing, we'd have to create async unit tests, which are hard to write,
 * to follow and to maintain. But neither can the testing mock respond synchronously; that would
 * change the execution of the code under test. For this reason, the mock $httpBackend has a
 * `flush()` method, which allows the test to explicitly flush pending requests. This preserves
 * the async api of the backend, while allowing the test to execute synchronously.
 *
 *
 * ## Unit testing with mock $httpBackend
 * The following code shows how to setup and use the mock backend when unit testing a controller.
 * First we create the controller under test:
 *
  ```js
  // The module code
  angular
    .module('MyApp', [])
    .controller('MyController', MyController);

  // The controller code
  function MyController($scope, $http) {
    var authToken;

    $http.get('/auth.py').then(function(response) {
      authToken = response.headers('A-Token');
      $scope.user = response.data;
    });

    $scope.saveMessage = function(message) {
      var headers = { 'Authorization': authToken };
      $scope.status = 'Saving...';

      $http.post('/add-msg.py', message, { headers: headers } ).then(function(response) {
        $scope.status = '';
      }).catch(function() {
        $scope.status = 'Failed...';
      });
    };
  }
  ```
 *
 * Now we setup the mock backend and create the test specs:
 *
  ```js
    // testing controller
    describe('MyController', function() {
       var $httpBackend, $rootScope, createController, authRequestHandler;

       // Set up the module
       beforeEach(module('MyApp'));

       beforeEach(inject(function($injector) {
         // Set up the mock http service responses
         $httpBackend = $injector.get('$httpBackend');
         // backend definition common for all tests
         authRequestHandler = $httpBackend.when('GET', '/auth.py')
                                .respond({userId: 'userX'}, {'A-Token': 'xxx'});

         // Get hold of a scope (i.e. the root scope)
         $rootScope = $injector.get('$rootScope');
         // The $controller service is used to create instances of controllers
         var $controller = $injector.get('$controller');

         createController = function() {
           return $controller('MyController', {'$scope' : $rootScope });
         };
       }));


       afterEach(function() {
         $httpBackend.verifyNoOutstandingExpectation();
         $httpBackend.verifyNoOutstandingRequest();
       });


       it('should fetch authentication token', function() {
         $httpBackend.expectGET('/auth.py');
         var controller = createController();
         $httpBackend.flush();
       });


       it('should fail authentication', function() {

         // Notice how you can change the response even after it was set
         authRequestHandler.respond(401, '');

         $httpBackend.expectGET('/auth.py');
         var controller = createController();
         $httpBackend.flush();
         expect($rootScope.status).toBe('Failed...');
       });


       it('should send msg to server', function() {
         var controller = createController();
         $httpBackend.flush();

         // now you don’t care about the authentication, but
         // the controller will still send the request and
         // $httpBackend will respond without you having to
         // specify the expectation and response for this request

         $httpBackend.expectPOST('/add-msg.py', 'message content').respond(201, '');
         $rootScope.saveMessage('message content');
         expect($rootScope.status).toBe('Saving...');
         $httpBackend.flush();
         expect($rootScope.status).toBe('');
       });


       it('should send auth header', function() {
         var controller = createController();
         $httpBackend.flush();

         $httpBackend.expectPOST('/add-msg.py', undefined, function(headers) {
           // check if the header was sent, if it wasn't the expectation won't
           // match the request and the test will fail
           return headers['Authorization'] == 'xxx';
         }).respond(201, '');

         $rootScope.saveMessage('whatever');
         $httpBackend.flush();
       });
    });
  ```
 *
 * ## Dynamic responses
 *
 * You define a response to a request by chaining a call to `respond()` onto a definition or expectation.
 * If you provide a **callback** as the first parameter to `respond(callback)` then you can dynamically generate
 * a response based on the properties of the request.
 *
 * The `callback` function should be of the form `function(method, url, data, headers, params)`.
 *
 * ### Query parameters
 *
 * By default, query parameters on request URLs are parsed into the `params` object. So a request URL
 * of `/list?q=searchstr&orderby=-name` would set `params` to be `{q: 'searchstr', orderby: '-name'}`.
 *
 * ### Regex parameter matching
 *
 * If an expectation or definition uses a **regex** to match the URL, you can provide an array of **keys** via a
 * `params` argument. The index of each **key** in the array will match the index of a **group** in the
 * **regex**.
 *
 * The `params` object in the **callback** will now have properties with these keys, which hold the value of the
 * corresponding **group** in the **regex**.
 *
 * This also applies to the `when` and `expect` shortcut methods.
 *
 *
 * ```js
 *   $httpBackend.expect('GET', /\/user\/(.+)/, undefined, undefined, ['id'])
 *     .respond(function(method, url, data, headers, params) {
 *       // for requested url of '/user/1234' params is {id: '1234'}
 *     });
 *
 *   $httpBackend.whenPATCH(/\/user\/(.+)\/article\/(.+)/, undefined, undefined, ['user', 'article'])
 *     .respond(function(method, url, data, headers, params) {
 *       // for url of '/user/1234/article/567' params is {user: '1234', article: '567'}
 *     });
 * ```
 *
 * ## Matching route requests
 *
 * For extra convenience, `whenRoute` and `expectRoute` shortcuts are available. These methods offer colon
 * delimited matching of the url path, ignoring the query string. This allows declarations
 * similar to how application routes are configured with `$routeProvider`. Because these methods convert
 * the definition url to regex, declaration order is important. Combined with query parameter parsing,
 * the following is possible:
 *
  ```js
    $httpBackend.whenRoute('GET', '/users/:id')
      .respond(function(method, url, data, headers, params) {
        return [200, MockUserList[Number(params.id)]];
      });

    $httpBackend.whenRoute('GET', '/users')
      .respond(function(method, url, data, headers, params) {
        var userList = angular.copy(MockUserList),
          defaultSort = 'lastName',
          count, pages, isPrevious, isNext;

        // paged api response '/v1/users?page=2'
        params.page = Number(params.page) || 1;

        // query for last names '/v1/users?q=Archer'
        if (params.q) {
          userList = $filter('filter')({lastName: params.q});
        }

        pages = Math.ceil(userList.length / pagingLength);
        isPrevious = params.page > 1;
        isNext = params.page < pages;

        return [200, {
          count:    userList.length,
          previous: isPrevious,
          next:     isNext,
          // sort field -> '/v1/users?sortBy=firstName'
          results:  $filter('orderBy')(userList, params.sortBy || defaultSort)
                      .splice((params.page - 1) * pagingLength, pagingLength)
        }];
      });
  ```
 */
angular.mock.$HttpBackendProvider = function() {
  this.$get = ['$rootScope', '$timeout', createHttpBackendMock];
};

/**
 * General factory function for $httpBackend mock.
 * Returns instance for unit testing (when no arguments specified):
 *   - passing through is disabled
 *   - auto flushing is disabled
 *
 * Returns instance for e2e testing (when `$delegate` and `$browser` specified):
 *   - passing through (delegating request to real backend) is enabled
 *   - auto flushing is enabled
 *
 * @param {Object=} $delegate Real $httpBackend instance (allow passing through if specified)
 * @param {Object=} $browser Auto-flushing enabled if specified
 * @return {Object} Instance of $httpBackend mock
 */
function createHttpBackendMock($rootScope, $timeout, $delegate, $browser) {
  var definitions = [],
      expectations = [],
      responses = [],
      responsesPush = angular.bind(responses, responses.push),
      copy = angular.copy;

  function createResponse(status, data, headers, statusText) {
    if (angular.isFunction(status)) return status;

    return function() {
      return angular.isNumber(status)
          ? [status, data, headers, statusText]
          : [200, status, data, headers];
    };
  }

  // TODO(vojta): change params to: method, url, data, headers, callback
  function $httpBackend(method, url, data, callback, headers, timeout, withCredentials, responseType, eventHandlers, uploadEventHandlers) {

    var xhr = new MockXhr(),
        expectation = expectations[0],
        wasExpected = false;

    xhr.$$events = eventHandlers;
    xhr.upload.$$events = uploadEventHandlers;

    function prettyPrint(data) {
      return (angular.isString(data) || angular.isFunction(data) || data instanceof RegExp)
          ? data
          : angular.toJson(data);
    }

    function wrapResponse(wrapped) {
      if (!$browser && timeout) {
        timeout.then ? timeout.then(handleTimeout) : $timeout(handleTimeout, timeout);
      }

      return handleResponse;

      function handleResponse() {
        var response = wrapped.response(method, url, data, headers, wrapped.params(url));
        xhr.$$respHeaders = response[2];
        callback(copy(response[0]), copy(response[1]), xhr.getAllResponseHeaders(),
                 copy(response[3] || ''));
      }

      function handleTimeout() {
        for (var i = 0, ii = responses.length; i < ii; i++) {
          if (responses[i] === handleResponse) {
            responses.splice(i, 1);
            callback(-1, undefined, '');
            break;
          }
        }
      }
    }

    if (expectation && expectation.match(method, url)) {
      if (!expectation.matchData(data)) {
        throw new Error('Expected ' + expectation + ' with different data\n' +
            'EXPECTED: ' + prettyPrint(expectation.data) + '\nGOT:      ' + data);
      }

      if (!expectation.matchHeaders(headers)) {
        throw new Error('Expected ' + expectation + ' with different headers\n' +
                        'EXPECTED: ' + prettyPrint(expectation.headers) + '\nGOT:      ' +
                        prettyPrint(headers));
      }

      expectations.shift();

      if (expectation.response) {
        responses.push(wrapResponse(expectation));
        return;
      }
      wasExpected = true;
    }

    var i = -1, definition;
    while ((definition = definitions[++i])) {
      if (definition.match(method, url, data, headers || {})) {
        if (definition.response) {
          // if $browser specified, we do auto flush all requests
          ($browser ? $browser.defer : responsesPush)(wrapResponse(definition));
        } else if (definition.passThrough) {
          $delegate(method, url, data, callback, headers, timeout, withCredentials, responseType, eventHandlers, uploadEventHandlers);
        } else throw new Error('No response defined !');
        return;
      }
    }
    throw wasExpected ?
        new Error('No response defined !') :
        new Error('Unexpected request: ' + method + ' ' + url + '\n' +
                  (expectation ? 'Expected ' + expectation : 'No more request expected'));
  }

  /**
   * @ngdoc method
   * @name $httpBackend#when
   * @description
   * Creates a new backend definition.
   *
   * @param {string} method HTTP method.
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string))=} data HTTP request body or function that receives
   *   data string and returns true if the data is as expected.
   * @param {(Object|function(Object))=} headers HTTP headers or function that receives http header
   *   object and returns true if the headers match the current definition.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   *
   *  - respond –
   *      ```js
   *      {function([status,] data[, headers, statusText])
   *      | function(function(method, url, data, headers, params)}
   *      ```
   *    – The respond method takes a set of static data to be returned or a function that can
   *    return an array containing response status (number), response data (Array|Object|string),
   *    response headers (Object), and the text for the status (string). The respond method returns
   *    the `requestHandler` object for possible overrides.
   */
  $httpBackend.when = function(method, url, data, headers, keys) {
    var definition = new MockHttpExpectation(method, url, data, headers, keys),
        chain = {
          respond: function(status, data, headers, statusText) {
            definition.passThrough = undefined;
            definition.response = createResponse(status, data, headers, statusText);
            return chain;
          }
        };

    if ($browser) {
      chain.passThrough = function() {
        definition.response = undefined;
        definition.passThrough = true;
        return chain;
      };
    }

    definitions.push(definition);
    return chain;
  };

  /**
   * @ngdoc method
   * @name $httpBackend#whenGET
   * @description
   * Creates a new backend definition for GET requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenHEAD
   * @description
   * Creates a new backend definition for HEAD requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenDELETE
   * @description
   * Creates a new backend definition for DELETE requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenPOST
   * @description
   * Creates a new backend definition for POST requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string))=} data HTTP request body or function that receives
   *   data string and returns true if the data is as expected.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenPUT
   * @description
   * Creates a new backend definition for PUT requests.  For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string))=} data HTTP request body or function that receives
   *   data string and returns true if the data is as expected.
   * @param {(Object|function(Object))=} headers HTTP headers.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#whenJSONP
   * @description
   * Creates a new backend definition for JSONP requests. For more info see `when()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled.
   */
  createShortMethods('when');

  /**
   * @ngdoc method
   * @name $httpBackend#whenRoute
   * @description
   * Creates a new backend definition that compares only with the requested route.
   *
   * @param {string} method HTTP method.
   * @param {string} url HTTP url string that supports colon param matching.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled. See #when for more info.
   */
  $httpBackend.whenRoute = function(method, url) {
    var pathObj = parseRoute(url);
    return $httpBackend.when(method, pathObj.regexp, undefined, undefined, pathObj.keys);
  };

  function parseRoute(url) {
    var ret = {
      regexp: url
    },
    keys = ret.keys = [];

    if (!url || !angular.isString(url)) return ret;

    url = url
      .replace(/([().])/g, '\\$1')
      .replace(/(\/)?:(\w+)([\?\*])?/g, function(_, slash, key, option) {
        var optional = option === '?' ? option : null;
        var star = option === '*' ? option : null;
        keys.push({ name: key, optional: !!optional });
        slash = slash || '';
        return ''
          + (optional ? '' : slash)
          + '(?:'
          + (optional ? slash : '')
          + (star && '(.+?)' || '([^/]+)')
          + (optional || '')
          + ')'
          + (optional || '');
      })
      .replace(/([\/$\*])/g, '\\$1');

    ret.regexp = new RegExp('^' + url, 'i');
    return ret;
  }

  /**
   * @ngdoc method
   * @name $httpBackend#expect
   * @description
   * Creates a new request expectation.
   *
   * @param {string} method HTTP method.
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {(Object|function(Object))=} headers HTTP headers or function that receives http header
   *   object and returns true if the headers match the current expectation.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *  request is handled. You can save this object for later use and invoke `respond` again in
   *  order to change how a matched request is handled.
   *
   *  - respond –
   *    ```
   *    { function([status,] data[, headers, statusText])
   *    | function(function(method, url, data, headers, params)}
   *    ```
   *    – The respond method takes a set of static data to be returned or a function that can
   *    return an array containing response status (number), response data (Array|Object|string),
   *    response headers (Object), and the text for the status (string). The respond method returns
   *    the `requestHandler` object for possible overrides.
   */
  $httpBackend.expect = function(method, url, data, headers, keys) {
    var expectation = new MockHttpExpectation(method, url, data, headers, keys),
        chain = {
          respond: function(status, data, headers, statusText) {
            expectation.response = createResponse(status, data, headers, statusText);
            return chain;
          }
        };

    expectations.push(expectation);
    return chain;
  };

  /**
   * @ngdoc method
   * @name $httpBackend#expectGET
   * @description
   * Creates a new request expectation for GET requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {Object=} headers HTTP headers.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled. See #expect for more info.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectHEAD
   * @description
   * Creates a new request expectation for HEAD requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {Object=} headers HTTP headers.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectDELETE
   * @description
   * Creates a new request expectation for DELETE requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {Object=} headers HTTP headers.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectPOST
   * @description
   * Creates a new request expectation for POST requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {Object=} headers HTTP headers.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectPUT
   * @description
   * Creates a new request expectation for PUT requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {Object=} headers HTTP headers.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectPATCH
   * @description
   * Creates a new request expectation for PATCH requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
   *   and returns true if the url matches the current definition.
   * @param {(string|RegExp|function(string)|Object)=} data HTTP request body or function that
   *  receives data string and returns true if the data is as expected, or Object if request body
   *  is in JSON format.
   * @param {Object=} headers HTTP headers.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */

  /**
   * @ngdoc method
   * @name $httpBackend#expectJSONP
   * @description
   * Creates a new request expectation for JSONP requests. For more info see `expect()`.
   *
   * @param {string|RegExp|function(string)} url HTTP url or function that receives an url
   *   and returns true if the url matches the current definition.
   * @param {(Array)=} keys Array of keys to assign to regex matches in request url described above.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   *   request is handled. You can save this object for later use and invoke `respond` again in
   *   order to change how a matched request is handled.
   */
  createShortMethods('expect');

  /**
   * @ngdoc method
   * @name $httpBackend#expectRoute
   * @description
   * Creates a new request expectation that compares only with the requested route.
   *
   * @param {string} method HTTP method.
   * @param {string} url HTTP url string that supports colon param matching.
   * @returns {requestHandler} Returns an object with `respond` method that controls how a matched
   * request is handled. You can save this object for later use and invoke `respond` again in
   * order to change how a matched request is handled. See #expect for more info.
   */
  $httpBackend.expectRoute = function(method, url) {
    var pathObj = parseRoute(url);
    return $httpBackend.expect(method, pathObj.regexp, undefined, undefined, pathObj.keys);
  };


  /**
   * @ngdoc method
   * @name $httpBackend#flush
   * @description
   * Flushes all pending requests using the trained responses.
   *
   * @param {number=} count Number of responses to flush (in the order they arrived). If undefined,
   *   all pending requests will be flushed. If there are no pending requests when the flush method
   *   is called an exception is thrown (as this typically a sign of programming error).
   */
  $httpBackend.flush = function(count, digest) {
    if (digest !== false) $rootScope.$digest();
    if (!responses.length) throw new Error('No pending request to flush !');

    if (angular.isDefined(count) && count !== null) {
      while (count--) {
        if (!responses.length) throw new Error('No more pending request to flush !');
        responses.shift()();
      }
    } else {
      while (responses.length) {
        responses.shift()();
      }
    }
    $httpBackend.verifyNoOutstandingExpectation(digest);
  };


  /**
   * @ngdoc method
   * @name $httpBackend#verifyNoOutstandingExpectation
   * @description
   * Verifies that all of the requests defined via the `expect` api were made. If any of the
   * requests were not made, verifyNoOutstandingExpectation throws an exception.
   *
   * Typically, you would call this method following each test case that asserts requests using an
   * "afterEach" clause.
   *
   * ```js
   *   afterEach($httpBackend.verifyNoOutstandingExpectation);
   * ```
   */
  $httpBackend.verifyNoOutstandingExpectation = function(digest) {
    if (digest !== false) $rootScope.$digest();
    if (expectations.length) {
      throw new Error('Unsatisfied requests: ' + expectations.join(', '));
    }
  };


  /**
   * @ngdoc method
   * @name $httpBackend#verifyNoOutstandingRequest
   * @description
   * Verifies that there are no outstanding requests that need to be flushed.
   *
   * Typically, you would call this method following each test case that asserts requests using an
   * "afterEach" clause.
   *
   * ```js
   *   afterEach($httpBackend.verifyNoOutstandingRequest);
   * ```
   */
  $httpBackend.verifyNoOutstandingRequest = function() {
    if (responses.length) {
      throw new Error('Unflushed requests: ' + responses.length);
    }
  };


  /**
   * @ngdoc method
   * @name $httpBackend#resetExpectations
   * @description
   * Resets all request expectations, but preserves all backend definitions. Typically, you would
   * call resetExpectations during a multiple-phase test when you want to reuse the same instance of
   * $httpBackend mock.
   */
  $httpBackend.resetExpectations = function() {
    expectations.length = 0;
    responses.length = 0;
  };

  return $httpBackend;


  function createShortMethods(prefix) {
    angular.forEach(['GET', 'DELETE', 'JSONP', 'HEAD'], function(method) {
     $httpBackend[prefix + method] = function(url, headers, keys) {
       return $httpBackend[prefix](method, url, undefined, headers, keys);
     };
    });

    angular.forEach(['PUT', 'POST', 'PATCH'], function(method) {
      $httpBackend[prefix + method] = function(url, data, headers, keys) {
        return $httpBackend[prefix](method, url, data, headers, keys);
      };
    });
  }
}

function MockHttpExpectation(method, url, data, headers, keys) {

  function getUrlParams(u) {
    var params = u.slice(u.indexOf('?') + 1).split('&');
    return params.sort();
  }

  function compareUrl(u) {
    return (url.slice(0, url.indexOf('?')) == u.slice(0, u.indexOf('?')) && getUrlParams(url).join() == getUrlParams(u).join());
  }

  this.data = data;
  this.headers = headers;

  this.match = function(m, u, d, h) {
    if (method != m) return false;
    if (!this.matchUrl(u)) return false;
    if (angular.isDefined(d) && !this.matchData(d)) return false;
    if (angular.isDefined(h) && !this.matchHeaders(h)) return false;
    return true;
  };

  this.matchUrl = function(u) {
    if (!url) return true;
    if (angular.isFunction(url.test)) return url.test(u);
    if (angular.isFunction(url)) return url(u);
    return (url == u || compareUrl(u));
  };

  this.matchHeaders = function(h) {
    if (angular.isUndefined(headers)) return true;
    if (angular.isFunction(headers)) return headers(h);
    return angular.equals(headers, h);
  };

  this.matchData = function(d) {
    if (angular.isUndefined(data)) return true;
    if (data && angular.isFunction(data.test)) return data.test(d);
    if (data && angular.isFunction(data)) return data(d);
    if (data && !angular.isString(data)) {
      return angular.equals(angular.fromJson(angular.toJson(data)), angular.fromJson(d));
    }
    return data == d;
  };

  this.toString = function() {
    return method + ' ' + url;
  };

  this.params = function(u) {
    return angular.extend(parseQuery(), pathParams());

    function pathParams() {
      var keyObj = {};
      if (!url || !angular.isFunction(url.test) || !keys || keys.length === 0) return keyObj;

      var m = url.exec(u);
      if (!m) return keyObj;
      for (var i = 1, len = m.length; i < len; ++i) {
        var key = keys[i - 1];
        var val = m[i];
        if (key && val) {
          keyObj[key.name || key] = val;
        }
      }

      return keyObj;
    }

    function parseQuery() {
      var obj = {}, key_value, key,
          queryStr = u.indexOf('?') > -1
          ? u.substring(u.indexOf('?') + 1)
          : "";

      angular.forEach(queryStr.split('&'), function(keyValue) {
        if (keyValue) {
          key_value = keyValue.replace(/\+/g,'%20').split('=');
          key = tryDecodeURIComponent(key_value[0]);
          if (angular.isDefined(key)) {
            var val = angular.isDefined(key_value[1]) ? tryDecodeURIComponent(key_value[1]) : true;
            if (!hasOwnProperty.call(obj, key)) {
              obj[key] = val;
            } else if (angular.isArray(obj[key])) {
              obj[key].push(val);
            } else {
              obj[key] = [obj[key],val];
            }
          }
        }
      });
      return obj;
    }
    function tryDecodeURIComponent(value) {
      try {
        return decodeURIComponent(value);
      } catch (e) {
        // Ignore any invalid uri component
      }
    }
  };
}

function createMockXhr() {
  return new MockXhr();
}

function MockXhr() {

  // hack for testing $http, $httpBackend
  MockXhr.$$lastInstance = this;

  this.open = function(method, url, async) {
    this.$$method = method;
    this.$$url = url;
    this.$$async = async;
    this.$$reqHeaders = {};
    this.$$respHeaders = {};
  };

  this.send = function(data) {
    this.$$data = data;
  };

  this.setRequestHeader = function(key, value) {
    this.$$reqHeaders[key] = value;
  };

  this.getResponseHeader = function(name) {
    // the lookup must be case insensitive,
    // that's why we try two quick lookups first and full scan last
    var header = this.$$respHeaders[name];
    if (header) return header;

    name = angular.lowercase(name);
    header = this.$$respHeaders[name];
    if (header) return header;

    header = undefined;
    angular.forEach(this.$$respHeaders, function(headerVal, headerName) {
      if (!header && angular.lowercase(headerName) == name) header = headerVal;
    });
    return header;
  };

  this.getAllResponseHeaders = function() {
    var lines = [];

    angular.forEach(this.$$respHeaders, function(value, key) {
      lines.push(key + ': ' + value);
    });
    return lines.join('\n');
  };

  this.abort = angular.noop;

  // This section simulates the events on a real XHR object (and the upload object)
  // When we are testing $httpBackend (inside the angular project) we make partial use of this
  // but store the events directly ourselves on `$$events`, instead of going through the `addEventListener`
  this.$$events = {};
  this.addEventListener = function(name, listener) {
    if (angular.isUndefined(this.$$events[name])) this.$$events[name] = [];
    this.$$events[name].push(listener);
  };

  this.upload = {
    $$events: {},
    addEventListener: this.addEventListener
  };
}


/**
 * @ngdoc service
 * @name $timeout
 * @description
 *
 * This service is just a simple decorator for {@link ng.$timeout $timeout} service
 * that adds a "flush" and "verifyNoPendingTasks" methods.
 */

angular.mock.$TimeoutDecorator = ['$delegate', '$browser', function($delegate, $browser) {

  /**
   * @ngdoc method
   * @name $timeout#flush
   * @description
   *
   * Flushes the queue of pending tasks.
   *
   * @param {number=} delay maximum timeout amount to flush up until
   */
  $delegate.flush = function(delay) {
    $browser.defer.flush(delay);
  };

  /**
   * @ngdoc method
   * @name $timeout#verifyNoPendingTasks
   * @description
   *
   * Verifies that there are no pending tasks that need to be flushed.
   */
  $delegate.verifyNoPendingTasks = function() {
    if ($browser.deferredFns.length) {
      throw new Error('Deferred tasks to flush (' + $browser.deferredFns.length + '): ' +
          formatPendingTasksAsString($browser.deferredFns));
    }
  };

  function formatPendingTasksAsString(tasks) {
    var result = [];
    angular.forEach(tasks, function(task) {
      result.push('{id: ' + task.id + ', ' + 'time: ' + task.time + '}');
    });

    return result.join(', ');
  }

  return $delegate;
}];

angular.mock.$RAFDecorator = ['$delegate', function($delegate) {
  var rafFn = function(fn) {
    var index = rafFn.queue.length;
    rafFn.queue.push(fn);
    return function() {
      rafFn.queue.splice(index, 1);
    };
  };

  rafFn.queue = [];
  rafFn.supported = $delegate.supported;

  rafFn.flush = function() {
    if (rafFn.queue.length === 0) {
      throw new Error('No rAF callbacks present');
    }

    var length = rafFn.queue.length;
    for (var i = 0; i < length; i++) {
      rafFn.queue[i]();
    }

    rafFn.queue = rafFn.queue.slice(i);
  };

  return rafFn;
}];

/**
 *
 */
var originalRootElement;
angular.mock.$RootElementProvider = function() {
  this.$get = ['$injector', function($injector) {
    originalRootElement = angular.element('<div ng-app></div>').data('$injector', $injector);
    return originalRootElement;
  }];
};

/**
 * @ngdoc service
 * @name $controller
 * @description
 * A decorator for {@link ng.$controller} with additional `bindings` parameter, useful when testing
 * controllers of directives that use {@link $compile#-bindtocontroller- `bindToController`}.
 *
 *
 * ## Example
 *
 * ```js
 *
 * // Directive definition ...
 *
 * myMod.directive('myDirective', {
 *   controller: 'MyDirectiveController',
 *   bindToController: {
 *     name: '@'
 *   }
 * });
 *
 *
 * // Controller definition ...
 *
 * myMod.controller('MyDirectiveController', ['$log', function($log) {
 *   $log.info(this.name);
 * }]);
 *
 *
 * // In a test ...
 *
 * describe('myDirectiveController', function() {
 *   it('should write the bound name to the log', inject(function($controller, $log) {
 *     var ctrl = $controller('MyDirectiveController', { /* no locals &#42;/ }, { name: 'Clark Kent' });
 *     expect(ctrl.name).toEqual('Clark Kent');
 *     expect($log.info.logs).toEqual(['Clark Kent']);
 *   }));
 * });
 *
 * ```
 *
 * @param {Function|string} constructor If called with a function then it's considered to be the
 *    controller constructor function. Otherwise it's considered to be a string which is used
 *    to retrieve the controller constructor using the following steps:
 *
 *    * check if a controller with given name is registered via `$controllerProvider`
 *    * check if evaluating the string on the current scope returns a constructor
 *    * if $controllerProvider#allowGlobals, check `window[constructor]` on the global
 *      `window` object (not recommended)
 *
 *    The string can use the `controller as property` syntax, where the controller instance is published
 *    as the specified property on the `scope`; the `scope` must be injected into `locals` param for this
 *    to work correctly.
 *
 * @param {Object} locals Injection locals for Controller.
 * @param {Object=} bindings Properties to add to the controller before invoking the constructor. This is used
 *                           to simulate the `bindToController` feature and simplify certain kinds of tests.
 * @return {Object} Instance of given controller.
 */
angular.mock.$ControllerDecorator = ['$delegate', function($delegate) {
  return function(expression, locals, later, ident) {
    if (later && typeof later === 'object') {
      var instantiate = $delegate(expression, locals, true, ident);
      angular.extend(instantiate.instance, later);

      var instance = instantiate();
      if (instance !== instantiate.instance) {
        angular.extend(instance, later);
      }

      return instance;
    }
    return $delegate(expression, locals, later, ident);
  };
}];

/**
 * @ngdoc service
 * @name $componentController
 * @description
 * A service that can be used to create instances of component controllers.
 * <div class="alert alert-info">
 * Be aware that the controller will be instantiated and attached to the scope as specified in
 * the component definition object. If you do not provide a `$scope` object in the `locals` param
 * then the helper will create a new isolated scope as a child of `$rootScope`.
 * </div>
 * @param {string} componentName the name of the component whose controller we want to instantiate
 * @param {Object} locals Injection locals for Controller.
 * @param {Object=} bindings Properties to add to the controller before invoking the constructor. This is used
 *                           to simulate the `bindToController` feature and simplify certain kinds of tests.
 * @param {string=} ident Override the property name to use when attaching the controller to the scope.
 * @return {Object} Instance of requested controller.
 */
angular.mock.$ComponentControllerProvider = ['$compileProvider', function($compileProvider) {
  this.$get = ['$controller','$injector', '$rootScope', function($controller, $injector, $rootScope) {
    return function $componentController(componentName, locals, bindings, ident) {
      // get all directives associated to the component name
      var directives = $injector.get(componentName + 'Directive');
      // look for those directives that are components
      var candidateDirectives = directives.filter(function(directiveInfo) {
        // components have controller, controllerAs and restrict:'E'
        return directiveInfo.controller && directiveInfo.controllerAs && directiveInfo.restrict === 'E';
      });
      // check if valid directives found
      if (candidateDirectives.length === 0) {
        throw new Error('No component found');
      }
      if (candidateDirectives.length > 1) {
        throw new Error('Too many components found');
      }
      // get the info of the component
      var directiveInfo = candidateDirectives[0];
      // create a scope if needed
      locals = locals || {};
      locals.$scope = locals.$scope || $rootScope.$new(true);
      return $controller(directiveInfo.controller, locals, bindings, ident || directiveInfo.controllerAs);
    };
  }];
}];


/**
 * @ngdoc module
 * @name ngMock
 * @packageName angular-mocks
 * @description
 *
 * # ngMock
 *
 * The `ngMock` module provides support to inject and mock Angular services into unit tests.
 * In addition, ngMock also extends various core ng services such that they can be
 * inspected and controlled in a synchronous manner within test code.
 *
 *
 * <div doc-module-components="ngMock"></div>
 *
 * @installation
 *
 *  First, download the file:
 *  * [Google CDN](https://developers.google.com/speed/libraries/devguide#angularjs) e.g.
 *    `"//ajax.googleapis.com/ajax/libs/angularjs/X.Y.Z/angular-mocks.js"`
 *  * [NPM](https://www.npmjs.com/) e.g. `npm install angular-mocks@X.Y.Z`
 *  * [Bower](http://bower.io) e.g. `bower install angular-mocks#X.Y.Z`
 *  * [code.angularjs.org](https://code.angularjs.org/) (discouraged for production use)  e.g.
 *    `"//code.angularjs.org/X.Y.Z/angular-mocks.js"`
 *
 * where X.Y.Z is the AngularJS version you are running.
 *
 * Then, configure your test runner to load `angular-mocks.js` after `angular.js`.
 * This example uses <a href="http://karma-runner.github.io/">Karma</a>:
 *
 * ```
 * config.set({
 *   files: [
 *     'build/angular.js', // and other module files you need
 *     'build/angular-mocks.js',
 *     '<path/to/application/files>',
 *     '<path/to/spec/files>'
 *   ]
 * });
 * ```
 *
 * Including the `angular-mocks.js` file automatically adds the `ngMock` module, so your tests
 *  are ready to go!
 */
angular.module('ngMock', ['ng']).provider({
  $browser: angular.mock.$BrowserProvider,
  $exceptionHandler: angular.mock.$ExceptionHandlerProvider,
  $log: angular.mock.$LogProvider,
  $interval: angular.mock.$IntervalProvider,
  $httpBackend: angular.mock.$HttpBackendProvider,
  $rootElement: angular.mock.$RootElementProvider,
  $componentController: angular.mock.$ComponentControllerProvider
}).config(['$provide', function($provide) {
  $provide.decorator('$timeout', angular.mock.$TimeoutDecorator);
  $provide.decorator('$$rAF', angular.mock.$RAFDecorator);
  $provide.decorator('$rootScope', angular.mock.$RootScopeDecorator);
  $provide.decorator('$controller', angular.mock.$ControllerDecorator);
}]);

/**
 * @ngdoc module
 * @name ngMockE2E
 * @module ngMockE2E
 * @packageName angular-mocks
 * @description
 *
 * The `ngMockE2E` is an angular module which contains mocks suitable for end-to-end testing.
 * Currently there is only one mock present in this module -
 * the {@link ngMockE2E.$httpBackend e2e $httpBackend} mock.
 */
angular.module('ngMockE2E', ['ng']).config(['$provide', function($provide) {
  $provide.value('$httpBackend', angular.injector(['ng']).get('$httpBackend'));
  $provide.decorator('$httpBackend', angular.mock.e2e.$httpBackendDecorator);
}]);

/**
 * @ngdoc service
 * @name $httpBackend
 * @module ngMockE2E
 * @description
 * Fake HTTP backend implementation suitable for end-to-end testing or backend-less development of
 * applications that use the {@link ng.$http $http service}.
 *
 * <div class="alert alert-info">
 * **Note**: For fake http backend implementation suitable for unit testing please see
 * {@link ngMock.$httpBackend unit-testing $httpBackend mock}.
 * </div>
 *
 * This implementation can be used to respond with static or dynamic responses via the `when` api
 * and its shortcuts (`whenGET`, `whenPOST`, etc) and optionally pass through requests to the
 * real $httpBackend for specific requests (e.g. to interact with certain remote apis or to fetch
 * templates from a webserver).
 *
 * As opposed to unit-testing, in an end-to-end testing scenario or in scenario when an application
 * is being developed with the real backend api replaced with a mock, it is often desirable for
 * certain category of requests to bypass the mock and issue a real http request (e.g. to fetch
 * templates or static files from the webserver). To configure the backend with this behavior
 * use the `passThrough` request handler of `when` instead of `respond`.
 *
 * Additionally, we don't want to manually have to flush mocked out requests like we do during unit
 * testing. For this reason the e2e $httpBackend flushes mocked out requests
 * automatically, closely simulating the behavior of the XMLHttpRequest object.
 *
 * To setup the application to run with this http backend, you have to create a module that depends
 * on the `ngMockE2E` and your application modules and defines the fake backend:
 *
 * ```js
 *   var myAppDev = angular.module('myAppDev', ['myApp', 'ngMockE2E']);
 *   myAppDev.run(function($httpBackend) {
 *     var phones = [{name: 'phone1'}, {name: 'phone2'}];
 *
 *     // returns the current list of phones
 *     $httpBackend.whenGET('/phones').respond(phones);
 *
 *     // adds a new phone to the phones array
 *     $httpBackend.whenPOST('/phones').respond(function(method, url, data) {
 *       var phone = angular.fromJson(data);
 *       phones.push(phone);
 *       return [200, phone, {}];
 *     });
 *     $httpBackend.whenGET(/^\/templates\//).passThrough(); // Requests for templare are handled by the real server
 *     //...
 *   });
 * ```
 *
 * Afterwards, bootstrap your app with this new module.
 *
 * ## Example
 * <example name="httpbackend-e2e-testing" module="myAppE2E" deps="angular-mocks.js">
 * <file name="app.js">
 *   var myApp = angular.module('myApp', []);
 *
 *   myApp.controller('main', function($http) {
 *     var ctrl = this;
 *
 *     ctrl.phones = [];
 *     ctrl.newPhone = {
 *       name: ''
 *     };
 *
 *     ctrl.getPhones = function() {
 *       $http.get('/phones').then(function(response) {
 *         ctrl.phones = response.data;
 *       });
 *     };
 *
 *     ctrl.addPhone = function(phone) {
 *       $http.post('/phones', phone).then(function() {
 *         ctrl.newPhone = {name: ''};
 *         return ctrl.getPhones();
 *       });
 *     };
 *
 *     ctrl.getPhones();
 *   });
 * </file>
 * <file name="e2e.js">
 *   var myAppDev = angular.module('myAppE2E', ['myApp', 'ngMockE2E']);
 *
 *   myAppDev.run(function($httpBackend) {
 *     var phones = [{name: 'phone1'}, {name: 'phone2'}];
 *
 *     // returns the current list of phones
 *     $httpBackend.whenGET('/phones').respond(phones);
 *
 *     // adds a new phone to the phones array
 *     $httpBackend.whenPOST('/phones').respond(function(method, url, data) {
 *       var phone = angular.fromJson(data);
 *       phones.push(phone);
 *       return [200, phone, {}];
 *     });
 *   });
 * </file>
 * <file name="index.html">
 *   <div ng-controller="main as $ctrl">
 *   <form name="newPhoneForm" ng-submit="$ctrl.addPhone($ctrl.newPhone)">
 *     <input type="text" ng-model="$ctrl.newPhone.name">
 *     <input type="submit" value="Add Phone">
 *   </form>
 *   <h1>Phones</h1>
 *   <ul>
 *     <li ng-repeat="phone in $ctrl.phones">{{phone.name}}</li>
 *   </ul>
 *   </div>
 * </file>
 * </example>
 *
 *
 */

/**
 * @ngdoc method
 * @name $httpBackend#when
 * @module ngMockE2E
 * @description
 * Creates a new backend definition.
 *
 * @param {string} method HTTP method.
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers or function that receives http header
 *   object and returns true if the headers match the current definition.
 * @param {(Array)=} keys Array of keys to assign to regex matches in request url described on
 *   {@link ngMock.$httpBackend $httpBackend mock}.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 *
 *  - respond –
 *    ```
 *    { function([status,] data[, headers, statusText])
 *    | function(function(method, url, data, headers, params)}
 *    ```
 *    – The respond method takes a set of static data to be returned or a function that can return
 *    an array containing response status (number), response data (Array|Object|string), response
 *    headers (Object), and the text for the status (string).
 *  - passThrough – `{function()}` – Any request matching a backend definition with
 *    `passThrough` handler will be passed through to the real backend (an XHR request will be made
 *    to the server.)
 *  - Both methods return the `requestHandler` object for possible overrides.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenGET
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for GET requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @param {(Array)=} keys Array of keys to assign to regex matches in request url described on
 *   {@link ngMock.$httpBackend $httpBackend mock}.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenHEAD
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for HEAD requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @param {(Array)=} keys Array of keys to assign to regex matches in request url described on
 *   {@link ngMock.$httpBackend $httpBackend mock}.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenDELETE
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for DELETE requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @param {(Array)=} keys Array of keys to assign to regex matches in request url described on
 *   {@link ngMock.$httpBackend $httpBackend mock}.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenPOST
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for POST requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @param {(Array)=} keys Array of keys to assign to regex matches in request url described on
 *   {@link ngMock.$httpBackend $httpBackend mock}.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenPUT
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for PUT requests.  For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @param {(Array)=} keys Array of keys to assign to regex matches in request url described on
 *   {@link ngMock.$httpBackend $httpBackend mock}.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenPATCH
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for PATCH requests.  For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(string|RegExp)=} data HTTP request body.
 * @param {(Object|function(Object))=} headers HTTP headers.
 * @param {(Array)=} keys Array of keys to assign to regex matches in request url described on
 *   {@link ngMock.$httpBackend $httpBackend mock}.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */

/**
 * @ngdoc method
 * @name $httpBackend#whenJSONP
 * @module ngMockE2E
 * @description
 * Creates a new backend definition for JSONP requests. For more info see `when()`.
 *
 * @param {string|RegExp|function(string)} url HTTP url or function that receives a url
 *   and returns true if the url matches the current definition.
 * @param {(Array)=} keys Array of keys to assign to regex matches in request url described on
 *   {@link ngMock.$httpBackend $httpBackend mock}.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */
/**
 * @ngdoc method
 * @name $httpBackend#whenRoute
 * @module ngMockE2E
 * @description
 * Creates a new backend definition that compares only with the requested route.
 *
 * @param {string} method HTTP method.
 * @param {string} url HTTP url string that supports colon param matching.
 * @returns {requestHandler} Returns an object with `respond` and `passThrough` methods that
 *   control how a matched request is handled. You can save this object for later use and invoke
 *   `respond` or `passThrough` again in order to change how a matched request is handled.
 */
angular.mock.e2e = {};
angular.mock.e2e.$httpBackendDecorator =
  ['$rootScope', '$timeout', '$delegate', '$browser', createHttpBackendMock];


/**
 * @ngdoc type
 * @name $rootScope.Scope
 * @module ngMock
 * @description
 * {@link ng.$rootScope.Scope Scope} type decorated with helper methods useful for testing. These
 * methods are automatically available on any {@link ng.$rootScope.Scope Scope} instance when
 * `ngMock` module is loaded.
 *
 * In addition to all the regular `Scope` methods, the following helper methods are available:
 */
angular.mock.$RootScopeDecorator = ['$delegate', function($delegate) {

  var $rootScopePrototype = Object.getPrototypeOf($delegate);

  $rootScopePrototype.$countChildScopes = countChildScopes;
  $rootScopePrototype.$countWatchers = countWatchers;

  return $delegate;

  // ------------------------------------------------------------------------------------------ //

  /**
   * @ngdoc method
   * @name $rootScope.Scope#$countChildScopes
   * @module ngMock
   * @description
   * Counts all the direct and indirect child scopes of the current scope.
   *
   * The current scope is excluded from the count. The count includes all isolate child scopes.
   *
   * @returns {number} Total number of child scopes.
   */
  function countChildScopes() {
    // jshint validthis: true
    var count = 0; // exclude the current scope
    var pendingChildHeads = [this.$$childHead];
    var currentScope;

    while (pendingChildHeads.length) {
      currentScope = pendingChildHeads.shift();

      while (currentScope) {
        count += 1;
        pendingChildHeads.push(currentScope.$$childHead);
        currentScope = currentScope.$$nextSibling;
      }
    }

    return count;
  }


  /**
   * @ngdoc method
   * @name $rootScope.Scope#$countWatchers
   * @module ngMock
   * @description
   * Counts all the watchers of direct and indirect child scopes of the current scope.
   *
   * The watchers of the current scope are included in the count and so are all the watchers of
   * isolate child scopes.
   *
   * @returns {number} Total number of watchers.
   */
  function countWatchers() {
    // jshint validthis: true
    var count = this.$$watchers ? this.$$watchers.length : 0; // include the current scope
    var pendingChildHeads = [this.$$childHead];
    var currentScope;

    while (pendingChildHeads.length) {
      currentScope = pendingChildHeads.shift();

      while (currentScope) {
        count += currentScope.$$watchers ? currentScope.$$watchers.length : 0;
        pendingChildHeads.push(currentScope.$$childHead);
        currentScope = currentScope.$$nextSibling;
      }
    }

    return count;
  }
}];


!(function(jasmineOrMocha) {

  if (!jasmineOrMocha) {
    return;
  }

  var currentSpec = null,
      injectorState = new InjectorState(),
      annotatedFunctions = [],
      wasInjectorCreated = function() {
        return !!currentSpec;
      };

  angular.mock.$$annotate = angular.injector.$$annotate;
  angular.injector.$$annotate = function(fn) {
    if (typeof fn === 'function' && !fn.$inject) {
      annotatedFunctions.push(fn);
    }
    return angular.mock.$$annotate.apply(this, arguments);
  };

  /**
   * @ngdoc function
   * @name angular.mock.module
   * @description
   *
   * *NOTE*: This function is also published on window for easy access.<br>
   * *NOTE*: This function is declared ONLY WHEN running tests with jasmine or mocha
   *
   * This function registers a module configuration code. It collects the configuration information
   * which will be used when the injector is created by {@link angular.mock.inject inject}.
   *
   * See {@link angular.mock.inject inject} for usage example
   *
   * @param {...(string|Function|Object)} fns any number of modules which are represented as string
   *        aliases or as anonymous module initialization functions. The modules are used to
   *        configure the injector. The 'ng' and 'ngMock' modules are automatically loaded. If an
   *        object literal is passed each key-value pair will be registered on the module via
   *        {@link auto.$provide $provide}.value, the key being the string name (or token) to associate
   *        with the value on the injector.
   */
  var module = window.module = angular.mock.module = function() {
    var moduleFns = Array.prototype.slice.call(arguments, 0);
    return wasInjectorCreated() ? workFn() : workFn;
    /////////////////////
    function workFn() {
      if (currentSpec.$injector) {
        throw new Error('Injector already created, can not register a module!');
      } else {
        var fn, modules = currentSpec.$modules || (currentSpec.$modules = []);
        angular.forEach(moduleFns, function(module) {
          if (angular.isObject(module) && !angular.isArray(module)) {
            fn = ['$provide', function($provide) {
              angular.forEach(module, function(value, key) {
                $provide.value(key, value);
              });
            }];
          } else {
            fn = module;
          }
          if (currentSpec.$providerInjector) {
            currentSpec.$providerInjector.invoke(fn);
          } else {
            modules.push(fn);
          }
        });
      }
    }
  };

  module.$$beforeAllHook = (window.before || window.beforeAll);
  module.$$afterAllHook = (window.after || window.afterAll);

  // purely for testing ngMock itself
  module.$$currentSpec = function(to) {
    if (arguments.length === 0) return to;
    currentSpec = to;
  };

  /**
   * @ngdoc function
   * @name angular.mock.module.sharedInjector
   * @description
   *
   * *NOTE*: This function is declared ONLY WHEN running tests with jasmine or mocha
   *
   * This function ensures a single injector will be used for all tests in a given describe context.
   * This contrasts with the default behaviour where a new injector is created per test case.
   *
   * Use sharedInjector when you want to take advantage of Jasmine's `beforeAll()`, or mocha's
   * `before()` methods. Call `module.sharedInjector()` before you setup any other hooks that
   * will create (i.e call `module()`) or use (i.e call `inject()`) the injector.
   *
   * You cannot call `sharedInjector()` from within a context already using `sharedInjector()`.
   *
   * ## Example
   *
   * Typically beforeAll is used to make many assertions about a single operation. This can
   * cut down test run-time as the test setup doesn't need to be re-run, and enabling focussed
   * tests each with a single assertion.
   *
   * ```js
   * describe("Deep Thought", function() {
   *
   *   module.sharedInjector();
   *
   *   beforeAll(module("UltimateQuestion"));
   *
   *   beforeAll(inject(function(DeepThought) {
   *     expect(DeepThought.answer).toBeUndefined();
   *     DeepThought.generateAnswer();
   *   }));
   *
   *   it("has calculated the answer correctly", inject(function(DeepThought) {
   *     // Because of sharedInjector, we have access to the instance of the DeepThought service
   *     // that was provided to the beforeAll() hook. Therefore we can test the generated answer
   *     expect(DeepThought.answer).toBe(42);
   *   }));
   *
   *   it("has calculated the answer within the expected time", inject(function(DeepThought) {
   *     expect(DeepThought.runTimeMillennia).toBeLessThan(8000);
   *   }));
   *
   *   it("has double checked the answer", inject(function(DeepThought) {
   *     expect(DeepThought.absolutelySureItIsTheRightAnswer).toBe(true);
   *   }));
   *
   * });
   *
   * ```
   */
  module.sharedInjector = function() {
    if (!(module.$$beforeAllHook && module.$$afterAllHook)) {
      throw Error("sharedInjector() cannot be used unless your test runner defines beforeAll/afterAll");
    }

    var initialized = false;

    module.$$beforeAllHook(function() {
      if (injectorState.shared) {
        injectorState.sharedError = Error("sharedInjector() cannot be called inside a context that has already called sharedInjector()");
        throw injectorState.sharedError;
      }
      initialized = true;
      currentSpec = this;
      injectorState.shared = true;
    });

    module.$$afterAllHook(function() {
      if (initialized) {
        injectorState = new InjectorState();
        module.$$cleanup();
      } else {
        injectorState.sharedError = null;
      }
    });
  };

  module.$$beforeEach = function() {
    if (injectorState.shared && currentSpec && currentSpec != this) {
      var state = currentSpec;
      currentSpec = this;
      angular.forEach(["$injector","$modules","$providerInjector", "$injectorStrict"], function(k) {
        currentSpec[k] = state[k];
        state[k] = null;
      });
    } else {
      currentSpec = this;
      originalRootElement = null;
      annotatedFunctions = [];
    }
  };

  module.$$afterEach = function() {
    if (injectorState.cleanupAfterEach()) {
      module.$$cleanup();
    }
  };

  module.$$cleanup = function() {
    var injector = currentSpec.$injector;

    annotatedFunctions.forEach(function(fn) {
      delete fn.$inject;
    });

    angular.forEach(currentSpec.$modules, function(module) {
      if (module && module.$$hashKey) {
        module.$$hashKey = undefined;
      }
    });

    currentSpec.$injector = null;
    currentSpec.$modules = null;
    currentSpec.$providerInjector = null;
    currentSpec = null;

    if (injector) {
      // Ensure `$rootElement` is instantiated, before checking `originalRootElement`
      var $rootElement = injector.get('$rootElement');
      var rootNode = $rootElement && $rootElement[0];
      var cleanUpNodes = !originalRootElement ? [] : [originalRootElement[0]];
      if (rootNode && (!originalRootElement || rootNode !== originalRootElement[0])) {
        cleanUpNodes.push(rootNode);
      }
      angular.element.cleanData(cleanUpNodes);

      // Ensure `$destroy()` is available, before calling it
      // (a mocked `$rootScope` might not implement it (or not even be an object at all))
      var $rootScope = injector.get('$rootScope');
      if ($rootScope && $rootScope.$destroy) $rootScope.$destroy();
    }

    // clean up jquery's fragment cache
    angular.forEach(angular.element.fragments, function(val, key) {
      delete angular.element.fragments[key];
    });

    MockXhr.$$lastInstance = null;

    angular.forEach(angular.callbacks, function(val, key) {
      delete angular.callbacks[key];
    });
    angular.callbacks.$$counter = 0;
  };

  (window.beforeEach || window.setup)(module.$$beforeEach);
  (window.afterEach || window.teardown)(module.$$afterEach);

  /**
   * @ngdoc function
   * @name angular.mock.inject
   * @description
   *
   * *NOTE*: This function is also published on window for easy access.<br>
   * *NOTE*: This function is declared ONLY WHEN running tests with jasmine or mocha
   *
   * The inject function wraps a function into an injectable function. The inject() creates new
   * instance of {@link auto.$injector $injector} per test, which is then used for
   * resolving references.
   *
   *
   * ## Resolving References (Underscore Wrapping)
   * Often, we would like to inject a reference once, in a `beforeEach()` block and reuse this
   * in multiple `it()` clauses. To be able to do this we must assign the reference to a variable
   * that is declared in the scope of the `describe()` block. Since we would, most likely, want
   * the variable to have the same name of the reference we have a problem, since the parameter
   * to the `inject()` function would hide the outer variable.
   *
   * To help with this, the injected parameters can, optionally, be enclosed with underscores.
   * These are ignored by the injector when the reference name is resolved.
   *
   * For example, the parameter `_myService_` would be resolved as the reference `myService`.
   * Since it is available in the function body as _myService_, we can then assign it to a variable
   * defined in an outer scope.
   *
   * ```
   * // Defined out reference variable outside
   * var myService;
   *
   * // Wrap the parameter in underscores
   * beforeEach( inject( function(_myService_){
   *   myService = _myService_;
   * }));
   *
   * // Use myService in a series of tests.
   * it('makes use of myService', function() {
   *   myService.doStuff();
   * });
   *
   * ```
   *
   * See also {@link angular.mock.module angular.mock.module}
   *
   * ## Example
   * Example of what a typical jasmine tests looks like with the inject method.
   * ```js
   *
   *   angular.module('myApplicationModule', [])
   *       .value('mode', 'app')
   *       .value('version', 'v1.0.1');
   *
   *
   *   describe('MyApp', function() {
   *
   *     // You need to load modules that you want to test,
   *     // it loads only the "ng" module by default.
   *     beforeEach(module('myApplicationModule'));
   *
   *
   *     // inject() is used to inject arguments of all given functions
   *     it('should provide a version', inject(function(mode, version) {
   *       expect(version).toEqual('v1.0.1');
   *       expect(mode).toEqual('app');
   *     }));
   *
   *
   *     // The inject and module method can also be used inside of the it or beforeEach
   *     it('should override a version and test the new version is injected', function() {
   *       // module() takes functions or strings (module aliases)
   *       module(function($provide) {
   *         $provide.value('version', 'overridden'); // override version here
   *       });
   *
   *       inject(function(version) {
   *         expect(version).toEqual('overridden');
   *       });
   *     });
   *   });
   *
   * ```
   *
   * @param {...Function} fns any number of functions which will be injected using the injector.
   */



  var ErrorAddingDeclarationLocationStack = function(e, errorForStack) {
    this.message = e.message;
    this.name = e.name;
    if (e.line) this.line = e.line;
    if (e.sourceId) this.sourceId = e.sourceId;
    if (e.stack && errorForStack)
      this.stack = e.stack + '\n' + errorForStack.stack;
    if (e.stackArray) this.stackArray = e.stackArray;
  };
  ErrorAddingDeclarationLocationStack.prototype = Error.prototype;

  window.inject = angular.mock.inject = function() {
    var blockFns = Array.prototype.slice.call(arguments, 0);
    var errorForStack = new Error('Declaration Location');
    // IE10+ and PhanthomJS do not set stack trace information, until the error is thrown
    if (!errorForStack.stack) {
      try {
        throw errorForStack;
      } catch (e) {}
    }
    return wasInjectorCreated() ? workFn.call(currentSpec) : workFn;
    /////////////////////
    function workFn() {
      var modules = currentSpec.$modules || [];
      var strictDi = !!currentSpec.$injectorStrict;
      modules.unshift(['$injector', function($injector) {
        currentSpec.$providerInjector = $injector;
      }]);
      modules.unshift('ngMock');
      modules.unshift('ng');
      var injector = currentSpec.$injector;
      if (!injector) {
        if (strictDi) {
          // If strictDi is enabled, annotate the providerInjector blocks
          angular.forEach(modules, function(moduleFn) {
            if (typeof moduleFn === "function") {
              angular.injector.$$annotate(moduleFn);
            }
          });
        }
        injector = currentSpec.$injector = angular.injector(modules, strictDi);
        currentSpec.$injectorStrict = strictDi;
      }
      for (var i = 0, ii = blockFns.length; i < ii; i++) {
        if (currentSpec.$injectorStrict) {
          // If the injector is strict / strictDi, and the spec wants to inject using automatic
          // annotation, then annotate the function here.
          injector.annotate(blockFns[i]);
        }
        try {
          /* jshint -W040 *//* Jasmine explicitly provides a `this` object when calling functions */
          injector.invoke(blockFns[i] || angular.noop, this);
          /* jshint +W040 */
        } catch (e) {
          if (e.stack && errorForStack) {
            throw new ErrorAddingDeclarationLocationStack(e, errorForStack);
          }
          throw e;
        } finally {
          errorForStack = null;
        }
      }
    }
  };


  angular.mock.inject.strictDi = function(value) {
    value = arguments.length ? !!value : true;
    return wasInjectorCreated() ? workFn() : workFn;

    function workFn() {
      if (value !== currentSpec.$injectorStrict) {
        if (currentSpec.$injector) {
          throw new Error('Injector already created, can not modify strict annotations');
        } else {
          currentSpec.$injectorStrict = value;
        }
      }
    }
  };

  function InjectorState() {
    this.shared = false;
    this.sharedError = null;

    this.cleanupAfterEach = function() {
      return !this.shared || this.sharedError;
    };
  }
})(window.jasmine || window.mocha);


})(window, window.angular);
;/*
 AngularJS v1.5.11
 (c) 2010-2017 Google, Inc. http://angularjs.org
 License: MIT
*/
(function(R,B){'use strict';function Da(a,b,c){if(!a)throw Ma("areq",b||"?",c||"required");return a}function Ea(a,b){if(!a&&!b)return"";if(!a)return b;if(!b)return a;X(a)&&(a=a.join(" "));X(b)&&(b=b.join(" "));return a+" "+b}function Na(a){var b={};a&&(a.to||a.from)&&(b.to=a.to,b.from=a.from);return b}function Y(a,b,c){var d="";a=X(a)?a:a&&G(a)&&a.length?a.split(/\s+/):[];s(a,function(a,l){a&&0<a.length&&(d+=0<l?" ":"",d+=c?b+a:a+b)});return d}function Oa(a){if(a instanceof F)switch(a.length){case 0:return a;
case 1:if(1===a[0].nodeType)return a;break;default:return F(ta(a))}if(1===a.nodeType)return F(a)}function ta(a){if(!a[0])return a;for(var b=0;b<a.length;b++){var c=a[b];if(1===c.nodeType)return c}}function Pa(a,b,c){s(b,function(b){a.addClass(b,c)})}function Qa(a,b,c){s(b,function(b){a.removeClass(b,c)})}function Z(a){return function(b,c){c.addClass&&(Pa(a,b,c.addClass),c.addClass=null);c.removeClass&&(Qa(a,b,c.removeClass),c.removeClass=null)}}function oa(a){a=a||{};if(!a.$$prepared){var b=a.domOperation||
P;a.domOperation=function(){a.$$domOperationFired=!0;b();b=P};a.$$prepared=!0}return a}function ha(a,b){Fa(a,b);Ga(a,b)}function Fa(a,b){b.from&&(a.css(b.from),b.from=null)}function Ga(a,b){b.to&&(a.css(b.to),b.to=null)}function V(a,b,c){var d=b.options||{};c=c.options||{};var e=(d.addClass||"")+" "+(c.addClass||""),l=(d.removeClass||"")+" "+(c.removeClass||"");a=Ra(a.attr("class"),e,l);c.preparationClasses&&(d.preparationClasses=$(c.preparationClasses,d.preparationClasses),delete c.preparationClasses);
e=d.domOperation!==P?d.domOperation:null;ua(d,c);e&&(d.domOperation=e);d.addClass=a.addClass?a.addClass:null;d.removeClass=a.removeClass?a.removeClass:null;b.addClass=d.addClass;b.removeClass=d.removeClass;return d}function Ra(a,b,c){function d(a){G(a)&&(a=a.split(" "));var b={};s(a,function(a){a.length&&(b[a]=!0)});return b}var e={};a=d(a);b=d(b);s(b,function(a,b){e[b]=1});c=d(c);s(c,function(a,b){e[b]=1===e[b]?null:-1});var l={addClass:"",removeClass:""};s(e,function(b,c){var d,e;1===b?(d="addClass",
e=!a[c]||a[c+"-remove"]):-1===b&&(d="removeClass",e=a[c]||a[c+"-add"]);e&&(l[d].length&&(l[d]+=" "),l[d]+=c)});return l}function y(a){return a instanceof F?a[0]:a}function Sa(a,b,c){var d="";b&&(d=Y(b,"ng-",!0));c.addClass&&(d=$(d,Y(c.addClass,"-add")));c.removeClass&&(d=$(d,Y(c.removeClass,"-remove")));d.length&&(c.preparationClasses=d,a.addClass(d))}function pa(a,b){var c=b?"-"+b+"s":"";la(a,[ma,c]);return[ma,c]}function va(a,b){var c=b?"paused":"",d=aa+"PlayState";la(a,[d,c]);return[d,c]}function la(a,
b){a.style[b[0]]=b[1]}function $(a,b){return a?b?a+" "+b:a:b}function Ha(a,b,c){var d=Object.create(null),e=a.getComputedStyle(b)||{};s(c,function(a,b){var c=e[a];if(c){var g=c.charAt(0);if("-"===g||"+"===g||0<=g)c=Ta(c);0===c&&(c=null);d[b]=c}});return d}function Ta(a){var b=0;a=a.split(/\s*,\s*/);s(a,function(a){"s"===a.charAt(a.length-1)&&(a=a.substring(0,a.length-1));a=parseFloat(a)||0;b=b?Math.max(a,b):a});return b}function wa(a){return 0===a||null!=a}function Ia(a,b){var c=S,d=a+"s";b?c+="Duration":
d+=" linear all";return[c,d]}function Ja(){var a=Object.create(null);return{flush:function(){a=Object.create(null)},count:function(b){return(b=a[b])?b.total:0},get:function(b){return(b=a[b])&&b.value},put:function(b,c){a[b]?a[b].total++:a[b]={total:1,value:c}}}}function Ka(a,b,c){s(c,function(c){a[c]=xa(a[c])?a[c]:b.style.getPropertyValue(c)})}var S,ya,aa,za;void 0===R.ontransitionend&&void 0!==R.onwebkittransitionend?(S="WebkitTransition",ya="webkitTransitionEnd transitionend"):(S="transition",ya=
"transitionend");void 0===R.onanimationend&&void 0!==R.onwebkitanimationend?(aa="WebkitAnimation",za="webkitAnimationEnd animationend"):(aa="animation",za="animationend");var qa=aa+"Delay",Aa=aa+"Duration",ma=S+"Delay",La=S+"Duration",Ma=B.$$minErr("ng"),Ua={transitionDuration:La,transitionDelay:ma,transitionProperty:S+"Property",animationDuration:Aa,animationDelay:qa,animationIterationCount:aa+"IterationCount"},Va={transitionDuration:La,transitionDelay:ma,animationDuration:Aa,animationDelay:qa},
Ba,ua,s,X,xa,ea,Ca,ba,G,J,F,P;B.module("ngAnimate",[],function(){P=B.noop;Ba=B.copy;ua=B.extend;F=B.element;s=B.forEach;X=B.isArray;G=B.isString;ba=B.isObject;J=B.isUndefined;xa=B.isDefined;Ca=B.isFunction;ea=B.isElement}).directive("ngAnimateSwap",["$animate","$rootScope",function(a,b){return{restrict:"A",transclude:"element",terminal:!0,priority:600,link:function(b,d,e,l,n){var I,g;b.$watchCollection(e.ngAnimateSwap||e["for"],function(e){I&&a.leave(I);g&&(g.$destroy(),g=null);if(e||0===e)g=b.$new(),
n(g,function(b){I=b;a.enter(b,null,d)})})}}}]).directive("ngAnimateChildren",["$interpolate",function(a){return{link:function(b,c,d){function e(a){c.data("$$ngAnimateChildren","on"===a||"true"===a)}var l=d.ngAnimateChildren;G(l)&&0===l.length?c.data("$$ngAnimateChildren",!0):(e(a(l)(b)),d.$observe("ngAnimateChildren",e))}}}]).factory("$$rAFScheduler",["$$rAF",function(a){function b(a){d=d.concat(a);c()}function c(){if(d.length){for(var b=d.shift(),n=0;n<b.length;n++)b[n]();e||a(function(){e||c()})}}
var d,e;d=b.queue=[];b.waitUntilQuiet=function(b){e&&e();e=a(function(){e=null;b();c()})};return b}]).provider("$$animateQueue",["$animateProvider",function(a){function b(a){if(!a)return null;a=a.split(" ");var b=Object.create(null);s(a,function(a){b[a]=!0});return b}function c(a,c){if(a&&c){var d=b(c);return a.split(" ").some(function(a){return d[a]})}}function d(a,b,c,d){return l[a].some(function(a){return a(b,c,d)})}function e(a,b){var c=0<(a.addClass||"").length,d=0<(a.removeClass||"").length;
return b?c&&d:c||d}var l=this.rules={skip:[],cancel:[],join:[]};l.join.push(function(a,b,c){return!b.structural&&e(b)});l.skip.push(function(a,b,c){return!b.structural&&!e(b)});l.skip.push(function(a,b,c){return"leave"===c.event&&b.structural});l.skip.push(function(a,b,c){return c.structural&&2===c.state&&!b.structural});l.cancel.push(function(a,b,c){return c.structural&&b.structural});l.cancel.push(function(a,b,c){return 2===c.state&&b.structural});l.cancel.push(function(a,b,d){if(d.structural)return!1;
a=b.addClass;b=b.removeClass;var e=d.addClass;d=d.removeClass;return J(a)&&J(b)||J(e)&&J(d)?!1:c(a,d)||c(b,e)});this.$get=["$$rAF","$rootScope","$rootElement","$document","$$HashMap","$$animation","$$AnimateRunner","$templateRequest","$$jqLite","$$forceReflow",function(b,c,g,l,C,Wa,Q,t,H,T){function O(){var a=!1;return function(b){a?b():c.$$postDigest(function(){a=!0;b()})}}function x(a,b,c){var f=y(b),d=y(a),N=[];(a=h[c])&&s(a,function(a){w.call(a.node,f)?N.push(a.callback):"leave"===c&&w.call(a.node,
d)&&N.push(a.callback)});return N}function r(a,b,c){var f=ta(b);return a.filter(function(a){return!(a.node===f&&(!c||a.callback===c))})}function p(a,h,v){function r(c,f,d,h){sa(function(){var c=x(T,a,f);c.length?b(function(){s(c,function(b){b(a,d,h)});"close"!==d||a[0].parentNode||ra.off(a)}):"close"!==d||a[0].parentNode||ra.off(a)});c.progress(f,d,h)}function k(b){var c=a,f=m;f.preparationClasses&&(c.removeClass(f.preparationClasses),f.preparationClasses=null);f.activeClasses&&(c.removeClass(f.activeClasses),
f.activeClasses=null);E(a,m);ha(a,m);m.domOperation();A.complete(!b)}var m=Ba(v),p,T;if(a=Oa(a))p=y(a),T=a.parent();var m=oa(m),A=new Q,sa=O();X(m.addClass)&&(m.addClass=m.addClass.join(" "));m.addClass&&!G(m.addClass)&&(m.addClass=null);X(m.removeClass)&&(m.removeClass=m.removeClass.join(" "));m.removeClass&&!G(m.removeClass)&&(m.removeClass=null);m.from&&!ba(m.from)&&(m.from=null);m.to&&!ba(m.to)&&(m.to=null);if(!p)return k(),A;v=[p.className,m.addClass,m.removeClass].join(" ");if(!Xa(v))return k(),
A;var g=0<=["enter","move","leave"].indexOf(h),w=l[0].hidden,t=!f||w||N.get(p);v=!t&&z.get(p)||{};var H=!!v.state;t||H&&1===v.state||(t=!M(a,T,h));if(t)return w&&r(A,h,"start"),k(),w&&r(A,h,"close"),A;g&&K(a);w={structural:g,element:a,event:h,addClass:m.addClass,removeClass:m.removeClass,close:k,options:m,runner:A};if(H){if(d("skip",a,w,v)){if(2===v.state)return k(),A;V(a,v,w);return v.runner}if(d("cancel",a,w,v))if(2===v.state)v.runner.end();else if(v.structural)v.close();else return V(a,v,w),v.runner;
else if(d("join",a,w,v))if(2===v.state)V(a,w,{});else return Sa(a,g?h:null,m),h=w.event=v.event,m=V(a,v,w),v.runner}else V(a,w,{});(H=w.structural)||(H="animate"===w.event&&0<Object.keys(w.options.to||{}).length||e(w));if(!H)return k(),ka(a),A;var C=(v.counter||0)+1;w.counter=C;L(a,1,w);c.$$postDigest(function(){var b=z.get(p),c=!b,b=b||{},f=0<(a.parent()||[]).length&&("animate"===b.event||b.structural||e(b));if(c||b.counter!==C||!f){c&&(E(a,m),ha(a,m));if(c||g&&b.event!==h)m.domOperation(),A.end();
f||ka(a)}else h=!b.structural&&e(b,!0)?"setClass":b.event,L(a,2),b=Wa(a,h,b.options),A.setHost(b),r(A,h,"start",{}),b.done(function(b){k(!b);(b=z.get(p))&&b.counter===C&&ka(y(a));r(A,h,"close",{})})});return A}function K(a){a=y(a).querySelectorAll("[data-ng-animate]");s(a,function(a){var b=parseInt(a.getAttribute("data-ng-animate"),10),c=z.get(a);if(c)switch(b){case 2:c.runner.end();case 1:z.remove(a)}})}function ka(a){a=y(a);a.removeAttribute("data-ng-animate");z.remove(a)}function k(a,b){return y(a)===
y(b)}function M(a,b,c){c=F(l[0].body);var f=k(a,c)||"HTML"===a[0].nodeName,d=k(a,g),h=!1,r,e=N.get(y(a));(a=F.data(a[0],"$ngAnimatePin"))&&(b=a);for(b=y(b);b;){d||(d=k(b,g));if(1!==b.nodeType)break;a=z.get(b)||{};if(!h){var p=N.get(b);if(!0===p&&!1!==e){e=!0;break}else!1===p&&(e=!1);h=a.structural}if(J(r)||!0===r)a=F.data(b,"$$ngAnimateChildren"),xa(a)&&(r=a);if(h&&!1===r)break;f||(f=k(b,c));if(f&&d)break;if(!d&&(a=F.data(b,"$ngAnimatePin"))){b=y(a);continue}b=b.parentNode}return(!h||r)&&!0!==e&&
d&&f}function L(a,b,c){c=c||{};c.state=b;a=y(a);a.setAttribute("data-ng-animate",b);c=(b=z.get(a))?ua(b,c):c;z.put(a,c)}var z=new C,N=new C,f=null,A=c.$watch(function(){return 0===t.totalPendingRequests},function(a){a&&(A(),c.$$postDigest(function(){c.$$postDigest(function(){null===f&&(f=!0)})}))}),h=Object.create(null),sa=a.classNameFilter(),Xa=sa?function(a){return sa.test(a)}:function(){return!0},E=Z(H),w=R.Node.prototype.contains||function(a){return this===a||!!(this.compareDocumentPosition(a)&
16)},ra={on:function(a,b,c){var f=ta(b);h[a]=h[a]||[];h[a].push({node:f,callback:c});F(b).on("$destroy",function(){z.get(f)||ra.off(a,b,c)})},off:function(a,b,c){if(1!==arguments.length||G(arguments[0])){var f=h[a];f&&(h[a]=1===arguments.length?null:r(f,b,c))}else for(f in b=arguments[0],h)h[f]=r(h[f],b)},pin:function(a,b){Da(ea(a),"element","not an element");Da(ea(b),"parentElement","not an element");a.data("$ngAnimatePin",b)},push:function(a,b,c,f){c=c||{};c.domOperation=f;return p(a,b,c)},enabled:function(a,
b){var c=arguments.length;if(0===c)b=!!f;else if(ea(a)){var d=y(a);1===c?b=!N.get(d):N.put(d,!b)}else b=f=!!a;return b}};return ra}]}]).provider("$$animation",["$animateProvider",function(a){var b=this.drivers=[];this.$get=["$$jqLite","$rootScope","$injector","$$AnimateRunner","$$HashMap","$$rAFScheduler",function(a,d,e,l,n,I){function g(a){function b(a){if(a.processed)return a;a.processed=!0;var d=a.domNode,p=d.parentNode;e.put(d,a);for(var K;p;){if(K=e.get(p)){K.processed||(K=b(K));break}p=p.parentNode}(K||
c).children.push(a);return a}var c={children:[]},d,e=new n;for(d=0;d<a.length;d++){var g=a[d];e.put(g.domNode,a[d]={domNode:g.domNode,fn:g.fn,children:[]})}for(d=0;d<a.length;d++)b(a[d]);return function(a){var b=[],c=[],d;for(d=0;d<a.children.length;d++)c.push(a.children[d]);a=c.length;var e=0,k=[];for(d=0;d<c.length;d++){var g=c[d];0>=a&&(a=e,e=0,b.push(k),k=[]);k.push(g.fn);g.children.forEach(function(a){e++;c.push(a)});a--}k.length&&b.push(k);return b}(c)}var u=[],C=Z(a);return function(n,Q,t){function H(a){a=
a.hasAttribute("ng-animate-ref")?[a]:a.querySelectorAll("[ng-animate-ref]");var b=[];s(a,function(a){var c=a.getAttribute("ng-animate-ref");c&&c.length&&b.push(a)});return b}function T(a){var b=[],c={};s(a,function(a,d){var h=y(a.element),e=0<=["enter","move"].indexOf(a.event),h=a.structural?H(h):[];if(h.length){var k=e?"to":"from";s(h,function(a){var b=a.getAttribute("ng-animate-ref");c[b]=c[b]||{};c[b][k]={animationID:d,element:F(a)}})}else b.push(a)});var d={},e={};s(c,function(c,k){var r=c.from,
p=c.to;if(r&&p){var z=a[r.animationID],g=a[p.animationID],A=r.animationID.toString();if(!e[A]){var n=e[A]={structural:!0,beforeStart:function(){z.beforeStart();g.beforeStart()},close:function(){z.close();g.close()},classes:O(z.classes,g.classes),from:z,to:g,anchors:[]};n.classes.length?b.push(n):(b.push(z),b.push(g))}e[A].anchors.push({out:r.element,"in":p.element})}else r=r?r.animationID:p.animationID,p=r.toString(),d[p]||(d[p]=!0,b.push(a[r]))});return b}function O(a,b){a=a.split(" ");b=b.split(" ");
for(var c=[],d=0;d<a.length;d++){var e=a[d];if("ng-"!==e.substring(0,3))for(var r=0;r<b.length;r++)if(e===b[r]){c.push(e);break}}return c.join(" ")}function x(a){for(var c=b.length-1;0<=c;c--){var d=e.get(b[c])(a);if(d)return d}}function r(a,b){function c(a){(a=a.data("$$animationRunner"))&&a.setHost(b)}a.from&&a.to?(c(a.from.element),c(a.to.element)):c(a.element)}function p(){var a=n.data("$$animationRunner");!a||"leave"===Q&&t.$$domOperationFired||a.end()}function K(b){n.off("$destroy",p);n.removeData("$$animationRunner");
C(n,t);ha(n,t);t.domOperation();L&&a.removeClass(n,L);n.removeClass("ng-animate");k.complete(!b)}t=oa(t);var ka=0<=["enter","move","leave"].indexOf(Q),k=new l({end:function(){K()},cancel:function(){K(!0)}});if(!b.length)return K(),k;n.data("$$animationRunner",k);var M=Ea(n.attr("class"),Ea(t.addClass,t.removeClass)),L=t.tempClasses;L&&(M+=" "+L,t.tempClasses=null);var z;ka&&(z="ng-"+Q+"-prepare",a.addClass(n,z));u.push({element:n,classes:M,event:Q,structural:ka,options:t,beforeStart:function(){n.addClass("ng-animate");
L&&a.addClass(n,L);z&&(a.removeClass(n,z),z=null)},close:K});n.on("$destroy",p);if(1<u.length)return k;d.$$postDigest(function(){var a=[];s(u,function(b){b.element.data("$$animationRunner")?a.push(b):b.close()});u.length=0;var b=T(a),c=[];s(b,function(a){c.push({domNode:y(a.from?a.from.element:a.element),fn:function(){a.beforeStart();var b,c=a.close;if((a.anchors?a.from.element||a.to.element:a.element).data("$$animationRunner")){var d=x(a);d&&(b=d.start)}b?(b=b(),b.done(function(a){c(!a)}),r(a,b)):
c()}})});I(g(c))});return k}}]}]).provider("$animateCss",["$animateProvider",function(a){var b=Ja(),c=Ja();this.$get=["$window","$$jqLite","$$AnimateRunner","$timeout","$$forceReflow","$sniffer","$$rAFScheduler","$$animateQueue",function(a,e,l,n,I,g,u,C){function B(a,b){var c=a.parentNode;return(c.$$ngAnimateParentKey||(c.$$ngAnimateParentKey=++O))+"-"+a.getAttribute("class")+"-"+b}function Q(r,p,g,n){var k;0<b.count(g)&&(k=c.get(g),k||(p=Y(p,"-stagger"),e.addClass(r,p),k=Ha(a,r,n),k.animationDuration=
Math.max(k.animationDuration,0),k.transitionDuration=Math.max(k.transitionDuration,0),e.removeClass(r,p),c.put(g,k)));return k||{}}function t(a){x.push(a);u.waitUntilQuiet(function(){b.flush();c.flush();for(var a=I(),d=0;d<x.length;d++)x[d](a);x.length=0})}function H(c,e,g){e=b.get(g);e||(e=Ha(a,c,Ua),"infinite"===e.animationIterationCount&&(e.animationIterationCount=1));b.put(g,e);c=e;g=c.animationDelay;e=c.transitionDelay;c.maxDelay=g&&e?Math.max(g,e):g||e;c.maxDuration=Math.max(c.animationDuration*
c.animationIterationCount,c.transitionDuration);return c}var T=Z(e),O=0,x=[];return function(a,c){function d(){k()}function u(){k(!0)}function k(b){if(!(w||F&&O)){w=!0;O=!1;f.$$skipPreparationClasses||e.removeClass(a,ga);e.removeClass(a,ea);va(h,!1);pa(h,!1);s(x,function(a){h.style[a[0]]=""});T(a,f);ha(a,f);Object.keys(A).length&&s(A,function(a,b){a?h.style.setProperty(b,a):h.style.removeProperty(b)});if(f.onDone)f.onDone();fa&&fa.length&&a.off(fa.join(" "),z);var c=a.data("$$animateCss");c&&(n.cancel(c[0].timer),
a.removeData("$$animateCss"));G&&G.complete(!b)}}function M(a){q.blockTransition&&pa(h,a);q.blockKeyframeAnimation&&va(h,!!a)}function L(){G=new l({end:d,cancel:u});t(P);k();return{$$willAnimate:!1,start:function(){return G},end:d}}function z(a){a.stopPropagation();var b=a.originalEvent||a;a=b.$manualTimeStamp||Date.now();b=parseFloat(b.elapsedTime.toFixed(3));Math.max(a-Z,0)>=R&&b>=m&&(F=!0,k())}function N(){function b(){if(!w){M(!1);s(x,function(a){h.style[a[0]]=a[1]});T(a,f);e.addClass(a,ea);if(q.recalculateTimingStyles){na=
h.className+" "+ga;ia=B(h,na);D=H(h,na,ia);ca=D.maxDelay;J=Math.max(ca,0);m=D.maxDuration;if(0===m){k();return}q.hasTransitions=0<D.transitionDuration;q.hasAnimations=0<D.animationDuration}q.applyAnimationDelay&&(ca="boolean"!==typeof f.delay&&wa(f.delay)?parseFloat(f.delay):ca,J=Math.max(ca,0),D.animationDelay=ca,da=[qa,ca+"s"],x.push(da),h.style[da[0]]=da[1]);R=1E3*J;V=1E3*m;if(f.easing){var d,g=f.easing;q.hasTransitions&&(d=S+"TimingFunction",x.push([d,g]),h.style[d]=g);q.hasAnimations&&(d=aa+
"TimingFunction",x.push([d,g]),h.style[d]=g)}D.transitionDuration&&fa.push(ya);D.animationDuration&&fa.push(za);Z=Date.now();var p=R+1.5*V;d=Z+p;var g=a.data("$$animateCss")||[],N=!0;if(g.length){var l=g[0];(N=d>l.expectedEndTime)?n.cancel(l.timer):g.push(k)}N&&(p=n(c,p,!1),g[0]={timer:p,expectedEndTime:d},g.push(k),a.data("$$animateCss",g));if(fa.length)a.on(fa.join(" "),z);f.to&&(f.cleanupStyles&&Ka(A,h,Object.keys(f.to)),Ga(a,f))}}function c(){var b=a.data("$$animateCss");if(b){for(var d=1;d<b.length;d++)b[d]();
a.removeData("$$animateCss")}}if(!w)if(h.parentNode){var d=function(a){if(F)O&&a&&(O=!1,k());else if(O=!a,D.animationDuration)if(a=va(h,O),O)x.push(a);else{var b=x,c=b.indexOf(a);0<=a&&b.splice(c,1)}},g=0<ba&&(D.transitionDuration&&0===W.transitionDuration||D.animationDuration&&0===W.animationDuration)&&Math.max(W.animationDelay,W.transitionDelay);g?n(b,Math.floor(g*ba*1E3),!1):b();v.resume=function(){d(!0)};v.pause=function(){d(!1)}}else k()}var f=c||{};f.$$prepared||(f=oa(Ba(f)));var A={},h=y(a);
if(!h||!h.parentNode||!C.enabled())return L();var x=[],I=a.attr("class"),E=Na(f),w,O,F,G,v,J,R,m,V,Z,fa=[];if(0===f.duration||!g.animations&&!g.transitions)return L();var ja=f.event&&X(f.event)?f.event.join(" "):f.event,$="",U="";ja&&f.structural?$=Y(ja,"ng-",!0):ja&&($=ja);f.addClass&&(U+=Y(f.addClass,"-add"));f.removeClass&&(U.length&&(U+=" "),U+=Y(f.removeClass,"-remove"));f.applyClassesEarly&&U.length&&T(a,f);var ga=[$,U].join(" ").trim(),na=I+" "+ga,ea=Y(ga,"-active"),I=E.to&&0<Object.keys(E.to).length;
if(!(0<(f.keyframeStyle||"").length||I||ga))return L();var ia,W;0<f.stagger?(E=parseFloat(f.stagger),W={transitionDelay:E,animationDelay:E,transitionDuration:0,animationDuration:0}):(ia=B(h,na),W=Q(h,ga,ia,Va));f.$$skipPreparationClasses||e.addClass(a,ga);f.transitionStyle&&(E=[S,f.transitionStyle],la(h,E),x.push(E));0<=f.duration&&(E=0<h.style[S].length,E=Ia(f.duration,E),la(h,E),x.push(E));f.keyframeStyle&&(E=[aa,f.keyframeStyle],la(h,E),x.push(E));var ba=W?0<=f.staggerIndex?f.staggerIndex:b.count(ia):
0;(ja=0===ba)&&!f.skipBlocking&&pa(h,9999);var D=H(h,na,ia),ca=D.maxDelay;J=Math.max(ca,0);m=D.maxDuration;var q={};q.hasTransitions=0<D.transitionDuration;q.hasAnimations=0<D.animationDuration;q.hasTransitionAll=q.hasTransitions&&"all"===D.transitionProperty;q.applyTransitionDuration=I&&(q.hasTransitions&&!q.hasTransitionAll||q.hasAnimations&&!q.hasTransitions);q.applyAnimationDuration=f.duration&&q.hasAnimations;q.applyTransitionDelay=wa(f.delay)&&(q.applyTransitionDuration||q.hasTransitions);q.applyAnimationDelay=
wa(f.delay)&&q.hasAnimations;q.recalculateTimingStyles=0<U.length;if(q.applyTransitionDuration||q.applyAnimationDuration)m=f.duration?parseFloat(f.duration):m,q.applyTransitionDuration&&(q.hasTransitions=!0,D.transitionDuration=m,E=0<h.style[S+"Property"].length,x.push(Ia(m,E))),q.applyAnimationDuration&&(q.hasAnimations=!0,D.animationDuration=m,x.push([Aa,m+"s"]));if(0===m&&!q.recalculateTimingStyles)return L();if(null!=f.delay){var da;"boolean"!==typeof f.delay&&(da=parseFloat(f.delay),J=Math.max(da,
0));q.applyTransitionDelay&&x.push([ma,da+"s"]);q.applyAnimationDelay&&x.push([qa,da+"s"])}null==f.duration&&0<D.transitionDuration&&(q.recalculateTimingStyles=q.recalculateTimingStyles||ja);R=1E3*J;V=1E3*m;f.skipBlocking||(q.blockTransition=0<D.transitionDuration,q.blockKeyframeAnimation=0<D.animationDuration&&0<W.animationDelay&&0===W.animationDuration);f.from&&(f.cleanupStyles&&Ka(A,h,Object.keys(f.from)),Fa(a,f));q.blockTransition||q.blockKeyframeAnimation?M(m):f.skipBlocking||pa(h,!1);return{$$willAnimate:!0,
end:d,start:function(){if(!w)return v={end:d,cancel:u,resume:null,pause:null},G=new l(v),t(N),G}}}}]}]).provider("$$animateCssDriver",["$$animationProvider",function(a){a.drivers.push("$$animateCssDriver");this.$get=["$animateCss","$rootScope","$$AnimateRunner","$rootElement","$sniffer","$$jqLite","$document",function(a,c,d,e,l,n,I){function g(a){return a.replace(/\bng-\S+\b/g,"")}function u(a,b){G(a)&&(a=a.split(" "));G(b)&&(b=b.split(" "));return a.filter(function(a){return-1===b.indexOf(a)}).join(" ")}
function C(c,e,n){function l(a){var b={},c=y(a).getBoundingClientRect();s(["width","height","top","left"],function(a){var d=c[a];switch(a){case "top":d+=t.scrollTop;break;case "left":d+=t.scrollLeft}b[a]=Math.floor(d)+"px"});return b}function p(){var c=g(n.attr("class")||""),d=u(c,k),c=u(k,c),d=a(C,{to:l(n),addClass:"ng-anchor-in "+d,removeClass:"ng-anchor-out "+c,delay:!0});return d.$$willAnimate?d:null}function I(){C.remove();e.removeClass("ng-animate-shim");n.removeClass("ng-animate-shim")}var C=
F(y(e).cloneNode(!0)),k=g(C.attr("class")||"");e.addClass("ng-animate-shim");n.addClass("ng-animate-shim");C.addClass("ng-anchor");H.append(C);var M;c=function(){var c=a(C,{addClass:"ng-anchor-out",delay:!0,from:l(e)});return c.$$willAnimate?c:null}();if(!c&&(M=p(),!M))return I();var L=c||M;return{start:function(){function a(){c&&c.end()}var b,c=L.start();c.done(function(){c=null;if(!M&&(M=p()))return c=M.start(),c.done(function(){c=null;I();b.complete()}),c;I();b.complete()});return b=new d({end:a,
cancel:a})}}}function B(a,b,c,e){var g=Q(a,P),n=Q(b,P),l=[];s(e,function(a){(a=C(c,a.out,a["in"]))&&l.push(a)});if(g||n||0!==l.length)return{start:function(){function a(){s(b,function(a){a.end()})}var b=[];g&&b.push(g.start());n&&b.push(n.start());s(l,function(a){b.push(a.start())});var c=new d({end:a,cancel:a});d.all(b,function(a){c.complete(a)});return c}}}function Q(c){var d=c.element,e=c.options||{};c.structural&&(e.event=c.event,e.structural=!0,e.applyClassesEarly=!0,"leave"===c.event&&(e.onDone=
e.domOperation));e.preparationClasses&&(e.event=$(e.event,e.preparationClasses));c=a(d,e);return c.$$willAnimate?c:null}if(!l.animations&&!l.transitions)return P;var t=I[0].body;c=y(e);var H=F(c.parentNode&&11===c.parentNode.nodeType||t.contains(c)?c:t);return function(a){return a.from&&a.to?B(a.from,a.to,a.classes,a.anchors):Q(a)}}]}]).provider("$$animateJs",["$animateProvider",function(a){this.$get=["$injector","$$AnimateRunner","$$jqLite",function(b,c,d){function e(c){c=X(c)?c:c.split(" ");for(var d=
[],e={},l=0;l<c.length;l++){var s=c[l],B=a.$$registeredAnimations[s];B&&!e[s]&&(d.push(b.get(B)),e[s]=!0)}return d}var l=Z(d);return function(a,b,d,u){function C(){u.domOperation();l(a,u)}function B(a,b,d,e,f){switch(d){case "animate":b=[b,e.from,e.to,f];break;case "setClass":b=[b,F,G,f];break;case "addClass":b=[b,F,f];break;case "removeClass":b=[b,G,f];break;default:b=[b,f]}b.push(e);if(a=a.apply(a,b))if(Ca(a.start)&&(a=a.start()),a instanceof c)a.done(f);else if(Ca(a))return a;return P}function y(a,
b,d,e,f){var g=[];s(e,function(e){var k=e[f];k&&g.push(function(){var e,f,g=!1,h=function(a){g||(g=!0,(f||P)(a),e.complete(!a))};e=new c({end:function(){h()},cancel:function(){h(!0)}});f=B(k,a,b,d,function(a){h(!1===a)});return e})});return g}function t(a,b,d,e,f){var g=y(a,b,d,e,f);if(0===g.length){var h,k;"beforeSetClass"===f?(h=y(a,"removeClass",d,e,"beforeRemoveClass"),k=y(a,"addClass",d,e,"beforeAddClass")):"setClass"===f&&(h=y(a,"removeClass",d,e,"removeClass"),k=y(a,"addClass",d,e,"addClass"));
h&&(g=g.concat(h));k&&(g=g.concat(k))}if(0!==g.length)return function(a){var b=[];g.length&&s(g,function(a){b.push(a())});b.length?c.all(b,a):a();return function(a){s(b,function(b){a?b.cancel():b.end()})}}}var H=!1;3===arguments.length&&ba(d)&&(u=d,d=null);u=oa(u);d||(d=a.attr("class")||"",u.addClass&&(d+=" "+u.addClass),u.removeClass&&(d+=" "+u.removeClass));var F=u.addClass,G=u.removeClass,x=e(d),r,p;if(x.length){var K,J;"leave"===b?(J="leave",K="afterLeave"):(J="before"+b.charAt(0).toUpperCase()+
b.substr(1),K=b);"enter"!==b&&"move"!==b&&(r=t(a,b,u,x,J));p=t(a,b,u,x,K)}if(r||p){var k;return{$$willAnimate:!0,end:function(){k?k.end():(H=!0,C(),ha(a,u),k=new c,k.complete(!0));return k},start:function(){function b(c){H=!0;C();ha(a,u);k.complete(c)}if(k)return k;k=new c;var d,e=[];r&&e.push(function(a){d=r(a)});e.length?e.push(function(a){C();a(!0)}):C();p&&e.push(function(a){d=p(a)});k.setHost({end:function(){H||((d||P)(void 0),b(void 0))},cancel:function(){H||((d||P)(!0),b(!0))}});c.chain(e,
b);return k}}}}}]}]).provider("$$animateJsDriver",["$$animationProvider",function(a){a.drivers.push("$$animateJsDriver");this.$get=["$$animateJs","$$AnimateRunner",function(a,c){function d(c){return a(c.element,c.event,c.classes,c.options)}return function(a){if(a.from&&a.to){var b=d(a.from),n=d(a.to);if(b||n)return{start:function(){function a(){return function(){s(d,function(a){a.end()})}}var d=[];b&&d.push(b.start());n&&d.push(n.start());c.all(d,function(a){e.complete(a)});var e=new c({end:a(),cancel:a()});
return e}}}else return d(a)}}]}])})(window,window.angular);
//# sourceMappingURL=angular-animate.min.js.map
;/*
 * angular-ui-bootstrap
 * http://angular-ui.github.io/bootstrap/

 * Version: 1.3.3 - 2016-05-22
 * License: MIT
 */angular.module("ui.bootstrap",["ui.bootstrap.tpls","ui.bootstrap.collapse","ui.bootstrap.accordion","ui.bootstrap.alert","ui.bootstrap.buttons","ui.bootstrap.carousel","ui.bootstrap.dateparser","ui.bootstrap.isClass","ui.bootstrap.datepicker","ui.bootstrap.position","ui.bootstrap.datepickerPopup","ui.bootstrap.debounce","ui.bootstrap.dropdown","ui.bootstrap.stackedMap","ui.bootstrap.modal","ui.bootstrap.paging","ui.bootstrap.pager","ui.bootstrap.pagination","ui.bootstrap.tooltip","ui.bootstrap.popover","ui.bootstrap.progressbar","ui.bootstrap.rating","ui.bootstrap.tabs","ui.bootstrap.timepicker","ui.bootstrap.typeahead"]),angular.module("ui.bootstrap.tpls",["uib/template/accordion/accordion-group.html","uib/template/accordion/accordion.html","uib/template/alert/alert.html","uib/template/carousel/carousel.html","uib/template/carousel/slide.html","uib/template/datepicker/datepicker.html","uib/template/datepicker/day.html","uib/template/datepicker/month.html","uib/template/datepicker/year.html","uib/template/datepickerPopup/popup.html","uib/template/modal/backdrop.html","uib/template/modal/window.html","uib/template/pager/pager.html","uib/template/pagination/pagination.html","uib/template/tooltip/tooltip-html-popup.html","uib/template/tooltip/tooltip-popup.html","uib/template/tooltip/tooltip-template-popup.html","uib/template/popover/popover-html.html","uib/template/popover/popover-template.html","uib/template/popover/popover.html","uib/template/progressbar/bar.html","uib/template/progressbar/progress.html","uib/template/progressbar/progressbar.html","uib/template/rating/rating.html","uib/template/tabs/tab.html","uib/template/tabs/tabset.html","uib/template/timepicker/timepicker.html","uib/template/typeahead/typeahead-match.html","uib/template/typeahead/typeahead-popup.html"]),angular.module("ui.bootstrap.collapse",[]).directive("uibCollapse",["$animate","$q","$parse","$injector",function(a,b,c,d){var e=d.has("$animateCss")?d.get("$animateCss"):null;return{link:function(d,f,g){function h(){f.hasClass("collapse")&&f.hasClass("in")||b.resolve(l(d)).then(function(){f.removeClass("collapse").addClass("collapsing").attr("aria-expanded",!0).attr("aria-hidden",!1),e?e(f,{addClass:"in",easing:"ease",to:{height:f[0].scrollHeight+"px"}}).start()["finally"](i):a.addClass(f,"in",{to:{height:f[0].scrollHeight+"px"}}).then(i)})}function i(){f.removeClass("collapsing").addClass("collapse").css({height:"auto"}),m(d)}function j(){return f.hasClass("collapse")||f.hasClass("in")?void b.resolve(n(d)).then(function(){f.css({height:f[0].scrollHeight+"px"}).removeClass("collapse").addClass("collapsing").attr("aria-expanded",!1).attr("aria-hidden",!0),e?e(f,{removeClass:"in",to:{height:"0"}}).start()["finally"](k):a.removeClass(f,"in",{to:{height:"0"}}).then(k)}):k()}function k(){f.css({height:"0"}),f.removeClass("collapsing").addClass("collapse"),o(d)}var l=c(g.expanding),m=c(g.expanded),n=c(g.collapsing),o=c(g.collapsed);d.$eval(g.uibCollapse)||f.addClass("in").addClass("collapse").attr("aria-expanded",!0).attr("aria-hidden",!1).css({height:"auto"}),d.$watch(g.uibCollapse,function(a){a?j():h()})}}}]),angular.module("ui.bootstrap.accordion",["ui.bootstrap.collapse"]).constant("uibAccordionConfig",{closeOthers:!0}).controller("UibAccordionController",["$scope","$attrs","uibAccordionConfig",function(a,b,c){this.groups=[],this.closeOthers=function(d){var e=angular.isDefined(b.closeOthers)?a.$eval(b.closeOthers):c.closeOthers;e&&angular.forEach(this.groups,function(a){a!==d&&(a.isOpen=!1)})},this.addGroup=function(a){var b=this;this.groups.push(a),a.$on("$destroy",function(c){b.removeGroup(a)})},this.removeGroup=function(a){var b=this.groups.indexOf(a);-1!==b&&this.groups.splice(b,1)}}]).directive("uibAccordion",function(){return{controller:"UibAccordionController",controllerAs:"accordion",transclude:!0,templateUrl:function(a,b){return b.templateUrl||"uib/template/accordion/accordion.html"}}}).directive("uibAccordionGroup",function(){return{require:"^uibAccordion",transclude:!0,replace:!0,templateUrl:function(a,b){return b.templateUrl||"uib/template/accordion/accordion-group.html"},scope:{heading:"@",panelClass:"@?",isOpen:"=?",isDisabled:"=?"},controller:function(){this.setHeading=function(a){this.heading=a}},link:function(a,b,c,d){d.addGroup(a),a.openClass=c.openClass||"panel-open",a.panelClass=c.panelClass||"panel-default",a.$watch("isOpen",function(c){b.toggleClass(a.openClass,!!c),c&&d.closeOthers(a)}),a.toggleOpen=function(b){a.isDisabled||b&&32!==b.which||(a.isOpen=!a.isOpen)};var e="accordiongroup-"+a.$id+"-"+Math.floor(1e4*Math.random());a.headingId=e+"-tab",a.panelId=e+"-panel"}}}).directive("uibAccordionHeading",function(){return{transclude:!0,template:"",replace:!0,require:"^uibAccordionGroup",link:function(a,b,c,d,e){d.setHeading(e(a,angular.noop))}}}).directive("uibAccordionTransclude",function(){function a(){return"uib-accordion-header,data-uib-accordion-header,x-uib-accordion-header,uib\\:accordion-header,[uib-accordion-header],[data-uib-accordion-header],[x-uib-accordion-header]"}return{require:"^uibAccordionGroup",link:function(b,c,d,e){b.$watch(function(){return e[d.uibAccordionTransclude]},function(b){if(b){var d=angular.element(c[0].querySelector(a()));d.html(""),d.append(b)}})}}}),angular.module("ui.bootstrap.alert",[]).controller("UibAlertController",["$scope","$attrs","$interpolate","$timeout",function(a,b,c,d){a.closeable=!!b.close;var e=angular.isDefined(b.dismissOnTimeout)?c(b.dismissOnTimeout)(a.$parent):null;e&&d(function(){a.close()},parseInt(e,10))}]).directive("uibAlert",function(){return{controller:"UibAlertController",controllerAs:"alert",templateUrl:function(a,b){return b.templateUrl||"uib/template/alert/alert.html"},transclude:!0,replace:!0,scope:{type:"@",close:"&"}}}),angular.module("ui.bootstrap.buttons",[]).constant("uibButtonConfig",{activeClass:"active",toggleEvent:"click"}).controller("UibButtonsController",["uibButtonConfig",function(a){this.activeClass=a.activeClass||"active",this.toggleEvent=a.toggleEvent||"click"}]).directive("uibBtnRadio",["$parse",function(a){return{require:["uibBtnRadio","ngModel"],controller:"UibButtonsController",controllerAs:"buttons",link:function(b,c,d,e){var f=e[0],g=e[1],h=a(d.uibUncheckable);c.find("input").css({display:"none"}),g.$render=function(){c.toggleClass(f.activeClass,angular.equals(g.$modelValue,b.$eval(d.uibBtnRadio)))},c.on(f.toggleEvent,function(){if(!d.disabled){var a=c.hasClass(f.activeClass);a&&!angular.isDefined(d.uncheckable)||b.$apply(function(){g.$setViewValue(a?null:b.$eval(d.uibBtnRadio)),g.$render()})}}),d.uibUncheckable&&b.$watch(h,function(a){d.$set("uncheckable",a?"":void 0)})}}}]).directive("uibBtnCheckbox",function(){return{require:["uibBtnCheckbox","ngModel"],controller:"UibButtonsController",controllerAs:"button",link:function(a,b,c,d){function e(){return g(c.btnCheckboxTrue,!0)}function f(){return g(c.btnCheckboxFalse,!1)}function g(b,c){return angular.isDefined(b)?a.$eval(b):c}var h=d[0],i=d[1];b.find("input").css({display:"none"}),i.$render=function(){b.toggleClass(h.activeClass,angular.equals(i.$modelValue,e()))},b.on(h.toggleEvent,function(){c.disabled||a.$apply(function(){i.$setViewValue(b.hasClass(h.activeClass)?f():e()),i.$render()})})}}}),angular.module("ui.bootstrap.carousel",[]).controller("UibCarouselController",["$scope","$element","$interval","$timeout","$animate",function(a,b,c,d,e){function f(){for(;t.length;)t.shift()}function g(a){for(var b=0;b<q.length;b++)q[b].slide.active=b===a}function h(c,d,i){if(!u){if(angular.extend(c,{direction:i}),angular.extend(q[s].slide||{},{direction:i}),e.enabled(b)&&!a.$currentTransition&&q[d].element&&p.slides.length>1){q[d].element.data(r,c.direction);var j=p.getCurrentIndex();angular.isNumber(j)&&q[j].element&&q[j].element.data(r,c.direction),a.$currentTransition=!0,e.on("addClass",q[d].element,function(b,c){if("close"===c&&(a.$currentTransition=null,e.off("addClass",b),t.length)){var d=t.pop().slide,g=d.index,i=g>p.getCurrentIndex()?"next":"prev";f(),h(d,g,i)}})}a.active=c.index,s=c.index,g(d),l()}}function i(a){for(var b=0;b<q.length;b++)if(q[b].slide===a)return b}function j(){n&&(c.cancel(n),n=null)}function k(b){b.length||(a.$currentTransition=null,f())}function l(){j();var b=+a.interval;!isNaN(b)&&b>0&&(n=c(m,b))}function m(){var b=+a.interval;o&&!isNaN(b)&&b>0&&q.length?a.next():a.pause()}var n,o,p=this,q=p.slides=a.slides=[],r="uib-slideDirection",s=a.active,t=[],u=!1;p.addSlide=function(b,c){q.push({slide:b,element:c}),q.sort(function(a,b){return+a.slide.index-+b.slide.index}),(b.index===a.active||1===q.length&&!angular.isNumber(a.active))&&(a.$currentTransition&&(a.$currentTransition=null),s=b.index,a.active=b.index,g(s),p.select(q[i(b)]),1===q.length&&a.play())},p.getCurrentIndex=function(){for(var a=0;a<q.length;a++)if(q[a].slide.index===s)return a},p.next=a.next=function(){var b=(p.getCurrentIndex()+1)%q.length;return 0===b&&a.noWrap()?void a.pause():p.select(q[b],"next")},p.prev=a.prev=function(){var b=p.getCurrentIndex()-1<0?q.length-1:p.getCurrentIndex()-1;return a.noWrap()&&b===q.length-1?void a.pause():p.select(q[b],"prev")},p.removeSlide=function(b){var c=i(b),d=t.indexOf(q[c]);-1!==d&&t.splice(d,1),q.splice(c,1),q.length>0&&s===c?c>=q.length?(s=q.length-1,a.active=s,g(s),p.select(q[q.length-1])):(s=c,a.active=s,g(s),p.select(q[c])):s>c&&(s--,a.active=s),0===q.length&&(s=null,a.active=null,f())},p.select=a.select=function(b,c){var d=i(b.slide);void 0===c&&(c=d>p.getCurrentIndex()?"next":"prev"),b.slide.index===s||a.$currentTransition?b&&b.slide.index!==s&&a.$currentTransition&&t.push(q[d]):h(b.slide,d,c)},a.indexOfSlide=function(a){return+a.slide.index},a.isActive=function(b){return a.active===b.slide.index},a.isPrevDisabled=function(){return 0===a.active&&a.noWrap()},a.isNextDisabled=function(){return a.active===q.length-1&&a.noWrap()},a.pause=function(){a.noPause||(o=!1,j())},a.play=function(){o||(o=!0,l())},a.$on("$destroy",function(){u=!0,j()}),a.$watch("noTransition",function(a){e.enabled(b,!a)}),a.$watch("interval",l),a.$watchCollection("slides",k),a.$watch("active",function(a){if(angular.isNumber(a)&&s!==a){for(var b=0;b<q.length;b++)if(q[b].slide.index===a){a=b;break}var c=q[a];c&&(g(a),p.select(q[a]),s=a)}})}]).directive("uibCarousel",function(){return{transclude:!0,replace:!0,controller:"UibCarouselController",controllerAs:"carousel",templateUrl:function(a,b){return b.templateUrl||"uib/template/carousel/carousel.html"},scope:{active:"=",interval:"=",noTransition:"=",noPause:"=",noWrap:"&"}}}).directive("uibSlide",function(){return{require:"^uibCarousel",transclude:!0,replace:!0,templateUrl:function(a,b){return b.templateUrl||"uib/template/carousel/slide.html"},scope:{actual:"=?",index:"=?"},link:function(a,b,c,d){d.addSlide(a,b),a.$on("$destroy",function(){d.removeSlide(a)})}}}).animation(".item",["$animateCss",function(a){function b(a,b,c){a.removeClass(b),c&&c()}var c="uib-slideDirection";return{beforeAddClass:function(d,e,f){if("active"===e){var g=!1,h=d.data(c),i="next"===h?"left":"right",j=b.bind(this,d,i+" "+h,f);return d.addClass(h),a(d,{addClass:i}).start().done(j),function(){g=!0}}f()},beforeRemoveClass:function(d,e,f){if("active"===e){var g=!1,h=d.data(c),i="next"===h?"left":"right",j=b.bind(this,d,i,f);return a(d,{addClass:i}).start().done(j),function(){g=!0}}f()}}}]),angular.module("ui.bootstrap.dateparser",[]).service("uibDateParser",["$log","$locale","dateFilter","orderByFilter",function(a,b,c,d){function e(a,b){var c=[],e=a.split(""),f=a.indexOf("'");if(f>-1){var g=!1;a=a.split("");for(var h=f;h<a.length;h++)g?("'"===a[h]&&(h+1<a.length&&"'"===a[h+1]?(a[h+1]="$",e[h+1]=""):(e[h]="",g=!1)),a[h]="$"):"'"===a[h]&&(a[h]="$",e[h]="",g=!0);a=a.join("")}return angular.forEach(n,function(d){var f=a.indexOf(d.key);if(f>-1){a=a.split(""),e[f]="("+d.regex+")",a[f]="$";for(var g=f+1,h=f+d.key.length;h>g;g++)e[g]="",a[g]="$";a=a.join(""),c.push({index:f,key:d.key,apply:d[b],matcher:d.regex})}}),{regex:new RegExp("^"+e.join("")+"$"),map:d(c,"index")}}function f(a,b,c){return 1>c?!1:1===b&&c>28?29===c&&(a%4===0&&a%100!==0||a%400===0):3===b||5===b||8===b||10===b?31>c:!0}function g(a){return parseInt(a,10)}function h(a,b){return a&&b?l(a,b):a}function i(a,b){return a&&b?l(a,b,!0):a}function j(a,b){a=a.replace(/:/g,"");var c=Date.parse("Jan 01, 1970 00:00:00 "+a)/6e4;return isNaN(c)?b:c}function k(a,b){return a=new Date(a.getTime()),a.setMinutes(a.getMinutes()+b),a}function l(a,b,c){c=c?-1:1;var d=a.getTimezoneOffset(),e=j(b,d);return k(a,c*(e-d))}var m,n,o=/[\\\^\$\*\+\?\|\[\]\(\)\.\{\}]/g;this.init=function(){m=b.id,this.parsers={},this.formatters={},n=[{key:"yyyy",regex:"\\d{4}",apply:function(a){this.year=+a},formatter:function(a){var b=new Date;return b.setFullYear(Math.abs(a.getFullYear())),c(b,"yyyy")}},{key:"yy",regex:"\\d{2}",apply:function(a){a=+a,this.year=69>a?a+2e3:a+1900},formatter:function(a){var b=new Date;return b.setFullYear(Math.abs(a.getFullYear())),c(b,"yy")}},{key:"y",regex:"\\d{1,4}",apply:function(a){this.year=+a},formatter:function(a){var b=new Date;return b.setFullYear(Math.abs(a.getFullYear())),c(b,"y")}},{key:"M!",regex:"0?[1-9]|1[0-2]",apply:function(a){this.month=a-1},formatter:function(a){var b=a.getMonth();return/^[0-9]$/.test(b)?c(a,"MM"):c(a,"M")}},{key:"MMMM",regex:b.DATETIME_FORMATS.MONTH.join("|"),apply:function(a){this.month=b.DATETIME_FORMATS.MONTH.indexOf(a)},formatter:function(a){return c(a,"MMMM")}},{key:"MMM",regex:b.DATETIME_FORMATS.SHORTMONTH.join("|"),apply:function(a){this.month=b.DATETIME_FORMATS.SHORTMONTH.indexOf(a)},formatter:function(a){return c(a,"MMM")}},{key:"MM",regex:"0[1-9]|1[0-2]",apply:function(a){this.month=a-1},formatter:function(a){return c(a,"MM")}},{key:"M",regex:"[1-9]|1[0-2]",apply:function(a){this.month=a-1},formatter:function(a){return c(a,"M")}},{key:"d!",regex:"[0-2]?[0-9]{1}|3[0-1]{1}",apply:function(a){this.date=+a},formatter:function(a){var b=a.getDate();return/^[1-9]$/.test(b)?c(a,"dd"):c(a,"d")}},{key:"dd",regex:"[0-2][0-9]{1}|3[0-1]{1}",apply:function(a){this.date=+a},formatter:function(a){return c(a,"dd")}},{key:"d",regex:"[1-2]?[0-9]{1}|3[0-1]{1}",apply:function(a){this.date=+a},formatter:function(a){return c(a,"d")}},{key:"EEEE",regex:b.DATETIME_FORMATS.DAY.join("|"),formatter:function(a){return c(a,"EEEE")}},{key:"EEE",regex:b.DATETIME_FORMATS.SHORTDAY.join("|"),formatter:function(a){return c(a,"EEE")}},{key:"HH",regex:"(?:0|1)[0-9]|2[0-3]",apply:function(a){this.hours=+a},formatter:function(a){return c(a,"HH")}},{key:"hh",regex:"0[0-9]|1[0-2]",apply:function(a){this.hours=+a},formatter:function(a){return c(a,"hh")}},{key:"H",regex:"1?[0-9]|2[0-3]",apply:function(a){this.hours=+a},formatter:function(a){return c(a,"H")}},{key:"h",regex:"[0-9]|1[0-2]",apply:function(a){this.hours=+a},formatter:function(a){return c(a,"h")}},{key:"mm",regex:"[0-5][0-9]",apply:function(a){this.minutes=+a},formatter:function(a){return c(a,"mm")}},{key:"m",regex:"[0-9]|[1-5][0-9]",apply:function(a){this.minutes=+a},formatter:function(a){return c(a,"m")}},{key:"sss",regex:"[0-9][0-9][0-9]",apply:function(a){this.milliseconds=+a},formatter:function(a){return c(a,"sss")}},{key:"ss",regex:"[0-5][0-9]",apply:function(a){this.seconds=+a},formatter:function(a){return c(a,"ss")}},{key:"s",regex:"[0-9]|[1-5][0-9]",apply:function(a){this.seconds=+a},formatter:function(a){return c(a,"s")}},{key:"a",regex:b.DATETIME_FORMATS.AMPMS.join("|"),apply:function(a){12===this.hours&&(this.hours=0),"PM"===a&&(this.hours+=12)},formatter:function(a){return c(a,"a")}},{key:"Z",regex:"[+-]\\d{4}",apply:function(a){var b=a.match(/([+-])(\d{2})(\d{2})/),c=b[1],d=b[2],e=b[3];this.hours+=g(c+d),this.minutes+=g(c+e)},formatter:function(a){return c(a,"Z")}},{key:"ww",regex:"[0-4][0-9]|5[0-3]",formatter:function(a){return c(a,"ww")}},{key:"w",regex:"[0-9]|[1-4][0-9]|5[0-3]",formatter:function(a){return c(a,"w")}},{key:"GGGG",regex:b.DATETIME_FORMATS.ERANAMES.join("|").replace(/\s/g,"\\s"),formatter:function(a){return c(a,"GGGG")}},{key:"GGG",regex:b.DATETIME_FORMATS.ERAS.join("|"),formatter:function(a){return c(a,"GGG")}},{key:"GG",regex:b.DATETIME_FORMATS.ERAS.join("|"),formatter:function(a){return c(a,"GG")}},{key:"G",regex:b.DATETIME_FORMATS.ERAS.join("|"),formatter:function(a){return c(a,"G")}}]},this.init(),this.filter=function(a,c){if(!angular.isDate(a)||isNaN(a)||!c)return"";c=b.DATETIME_FORMATS[c]||c,b.id!==m&&this.init(),this.formatters[c]||(this.formatters[c]=e(c,"formatter"));var d=this.formatters[c],f=d.map,g=c;return f.reduce(function(b,c,d){var e=g.match(new RegExp("(.*)"+c.key));e&&angular.isString(e[1])&&(b+=e[1],g=g.replace(e[1]+c.key,""));var h=d===f.length-1?g:"";return c.apply?b+c.apply.call(null,a)+h:b+h},"")},this.parse=function(c,d,g){if(!angular.isString(c)||!d)return c;d=b.DATETIME_FORMATS[d]||d,d=d.replace(o,"\\$&"),b.id!==m&&this.init(),this.parsers[d]||(this.parsers[d]=e(d,"apply"));var h=this.parsers[d],i=h.regex,j=h.map,k=c.match(i),l=!1;if(k&&k.length){var n,p;angular.isDate(g)&&!isNaN(g.getTime())?n={year:g.getFullYear(),month:g.getMonth(),date:g.getDate(),hours:g.getHours(),minutes:g.getMinutes(),seconds:g.getSeconds(),milliseconds:g.getMilliseconds()}:(g&&a.warn("dateparser:","baseDate is not a valid date"),n={year:1900,month:0,date:1,hours:0,minutes:0,seconds:0,milliseconds:0});for(var q=1,r=k.length;r>q;q++){var s=j[q-1];"Z"===s.matcher&&(l=!0),s.apply&&s.apply.call(n,k[q])}var t=l?Date.prototype.setUTCFullYear:Date.prototype.setFullYear,u=l?Date.prototype.setUTCHours:Date.prototype.setHours;return f(n.year,n.month,n.date)&&(!angular.isDate(g)||isNaN(g.getTime())||l?(p=new Date(0),t.call(p,n.year,n.month,n.date),u.call(p,n.hours||0,n.minutes||0,n.seconds||0,n.milliseconds||0)):(p=new Date(g),t.call(p,n.year,n.month,n.date),u.call(p,n.hours,n.minutes,n.seconds,n.milliseconds))),p}},this.toTimezone=h,this.fromTimezone=i,this.timezoneToOffset=j,this.addDateMinutes=k,this.convertTimezoneToLocal=l}]),angular.module("ui.bootstrap.isClass",[]).directive("uibIsClass",["$animate",function(a){var b=/^\s*([\s\S]+?)\s+on\s+([\s\S]+?)\s*$/,c=/^\s*([\s\S]+?)\s+for\s+([\s\S]+?)\s*$/;return{restrict:"A",compile:function(d,e){function f(a,b,c){i.push(a),j.push({scope:a,element:b}),o.forEach(function(b,c){g(b,a)}),a.$on("$destroy",h)}function g(b,d){var e=b.match(c),f=d.$eval(e[1]),g=e[2],h=k[b];if(!h){var i=function(b){var c=null;j.some(function(a){var d=a.scope.$eval(m);return d===b?(c=a,!0):void 0}),h.lastActivated!==c&&(h.lastActivated&&a.removeClass(h.lastActivated.element,f),c&&a.addClass(c.element,f),h.lastActivated=c)};k[b]=h={lastActivated:null,scope:d,watchFn:i,compareWithExp:g,watcher:d.$watch(g,i)}}h.watchFn(d.$eval(g))}function h(a){var b=a.targetScope,c=i.indexOf(b);if(i.splice(c,1),j.splice(c,1),i.length){var d=i[0];angular.forEach(k,function(a){a.scope===b&&(a.watcher=d.$watch(a.compareWithExp,a.watchFn),a.scope=d)})}else k={}}var i=[],j=[],k={},l=e.uibIsClass.match(b),m=l[2],n=l[1],o=n.split(",");return f}}}]),angular.module("ui.bootstrap.datepicker",["ui.bootstrap.dateparser","ui.bootstrap.isClass"]).value("$datepickerSuppressError",!1).value("$datepickerLiteralWarning",!0).constant("uibDatepickerConfig",{datepickerMode:"day",formatDay:"dd",formatMonth:"MMMM",formatYear:"yyyy",formatDayHeader:"EEE",formatDayTitle:"MMMM yyyy",formatMonthTitle:"yyyy",maxDate:null,maxMode:"year",minDate:null,minMode:"day",ngModelOptions:{},shortcutPropagation:!1,showWeeks:!0,yearColumns:5,yearRows:4}).controller("UibDatepickerController",["$scope","$attrs","$parse","$interpolate","$locale","$log","dateFilter","uibDatepickerConfig","$datepickerLiteralWarning","$datepickerSuppressError","uibDateParser",function(a,b,c,d,e,f,g,h,i,j,k){function l(b){a.datepickerMode=b,a.datepickerOptions.datepickerMode=b}var m=this,n={$setViewValue:angular.noop},o={},p=[];!!b.datepickerOptions;a.datepickerOptions||(a.datepickerOptions={}),this.modes=["day","month","year"],["customClass","dateDisabled","datepickerMode","formatDay","formatDayHeader","formatDayTitle","formatMonth","formatMonthTitle","formatYear","maxDate","maxMode","minDate","minMode","showWeeks","shortcutPropagation","startingDay","yearColumns","yearRows"].forEach(function(b){switch(b){case"customClass":case"dateDisabled":a[b]=a.datepickerOptions[b]||angular.noop;break;case"datepickerMode":a.datepickerMode=angular.isDefined(a.datepickerOptions.datepickerMode)?a.datepickerOptions.datepickerMode:h.datepickerMode;break;case"formatDay":case"formatDayHeader":case"formatDayTitle":case"formatMonth":case"formatMonthTitle":case"formatYear":m[b]=angular.isDefined(a.datepickerOptions[b])?d(a.datepickerOptions[b])(a.$parent):h[b];break;case"showWeeks":case"shortcutPropagation":case"yearColumns":case"yearRows":m[b]=angular.isDefined(a.datepickerOptions[b])?a.datepickerOptions[b]:h[b];break;case"startingDay":angular.isDefined(a.datepickerOptions.startingDay)?m.startingDay=a.datepickerOptions.startingDay:angular.isNumber(h.startingDay)?m.startingDay=h.startingDay:m.startingDay=(e.DATETIME_FORMATS.FIRSTDAYOFWEEK+8)%7;break;case"maxDate":case"minDate":a.$watch("datepickerOptions."+b,function(a){a?angular.isDate(a)?m[b]=k.fromTimezone(new Date(a),o.timezone):(i&&f.warn("Literal date support has been deprecated, please switch to date object usage"),m[b]=new Date(g(a,"medium"))):m[b]=h[b]?k.fromTimezone(new Date(h[b]),o.timezone):null,m.refreshView()});break;case"maxMode":case"minMode":a.datepickerOptions[b]?a.$watch(function(){return a.datepickerOptions[b]},function(c){m[b]=a[b]=angular.isDefined(c)?c:datepickerOptions[b],("minMode"===b&&m.modes.indexOf(a.datepickerOptions.datepickerMode)<m.modes.indexOf(m[b])||"maxMode"===b&&m.modes.indexOf(a.datepickerOptions.datepickerMode)>m.modes.indexOf(m[b]))&&(a.datepickerMode=m[b],a.datepickerOptions.datepickerMode=m[b])}):m[b]=a[b]=h[b]||null}}),a.uniqueId="datepicker-"+a.$id+"-"+Math.floor(1e4*Math.random()),a.disabled=angular.isDefined(b.disabled)||!1,angular.isDefined(b.ngDisabled)&&p.push(a.$parent.$watch(b.ngDisabled,function(b){a.disabled=b,m.refreshView()})),a.isActive=function(b){return 0===m.compare(b.date,m.activeDate)?(a.activeDateId=b.uid,!0):!1},this.init=function(b){n=b,o=b.$options||h.ngModelOptions,a.datepickerOptions.initDate?(m.activeDate=k.fromTimezone(a.datepickerOptions.initDate,o.timezone)||new Date,a.$watch("datepickerOptions.initDate",function(a){a&&(n.$isEmpty(n.$modelValue)||n.$invalid)&&(m.activeDate=k.fromTimezone(a,o.timezone),m.refreshView())})):m.activeDate=new Date;var c=n.$modelValue?new Date(n.$modelValue):new Date;this.activeDate=isNaN(c)?k.fromTimezone(new Date,o.timezone):k.fromTimezone(c,o.timezone),n.$render=function(){m.render()}},this.render=function(){if(n.$viewValue){var a=new Date(n.$viewValue),b=!isNaN(a);b?this.activeDate=k.fromTimezone(a,o.timezone):j||f.error('Datepicker directive: "ng-model" value must be a Date object')}this.refreshView()},this.refreshView=function(){if(this.element){a.selectedDt=null,this._refreshView(),a.activeDt&&(a.activeDateId=a.activeDt.uid);var b=n.$viewValue?new Date(n.$viewValue):null;b=k.fromTimezone(b,o.timezone),n.$setValidity("dateDisabled",!b||this.element&&!this.isDisabled(b))}},this.createDateObject=function(b,c){var d=n.$viewValue?new Date(n.$viewValue):null;d=k.fromTimezone(d,o.timezone);var e=new Date;e=k.fromTimezone(e,o.timezone);var f=this.compare(b,e),g={date:b,label:k.filter(b,c),selected:d&&0===this.compare(b,d),disabled:this.isDisabled(b),past:0>f,current:0===f,future:f>0,customClass:this.customClass(b)||null};return d&&0===this.compare(b,d)&&(a.selectedDt=g),m.activeDate&&0===this.compare(g.date,m.activeDate)&&(a.activeDt=g),g},this.isDisabled=function(b){return a.disabled||this.minDate&&this.compare(b,this.minDate)<0||this.maxDate&&this.compare(b,this.maxDate)>0||a.dateDisabled&&a.dateDisabled({date:b,mode:a.datepickerMode})},this.customClass=function(b){return a.customClass({date:b,mode:a.datepickerMode})},this.split=function(a,b){for(var c=[];a.length>0;)c.push(a.splice(0,b));return c},a.select=function(b){if(a.datepickerMode===m.minMode){var c=n.$viewValue?k.fromTimezone(new Date(n.$viewValue),o.timezone):new Date(0,0,0,0,0,0,0);c.setFullYear(b.getFullYear(),b.getMonth(),b.getDate()),c=k.toTimezone(c,o.timezone),n.$setViewValue(c),n.$render()}else m.activeDate=b,l(m.modes[m.modes.indexOf(a.datepickerMode)-1]),a.$emit("uib:datepicker.mode");a.$broadcast("uib:datepicker.focus")},a.move=function(a){var b=m.activeDate.getFullYear()+a*(m.step.years||0),c=m.activeDate.getMonth()+a*(m.step.months||0);m.activeDate.setFullYear(b,c,1),m.refreshView()},a.toggleMode=function(b){b=b||1,a.datepickerMode===m.maxMode&&1===b||a.datepickerMode===m.minMode&&-1===b||(l(m.modes[m.modes.indexOf(a.datepickerMode)+b]),a.$emit("uib:datepicker.mode"))},a.keys={13:"enter",32:"space",33:"pageup",34:"pagedown",35:"end",36:"home",37:"left",38:"up",39:"right",40:"down"};var q=function(){m.element[0].focus()};a.$on("uib:datepicker.focus",q),a.keydown=function(b){var c=a.keys[b.which];if(c&&!b.shiftKey&&!b.altKey&&!a.disabled)if(b.preventDefault(),m.shortcutPropagation||b.stopPropagation(),"enter"===c||"space"===c){if(m.isDisabled(m.activeDate))return;a.select(m.activeDate)}else!b.ctrlKey||"up"!==c&&"down"!==c?(m.handleKeyDown(c,b),m.refreshView()):a.toggleMode("up"===c?1:-1)},a.$on("$destroy",function(){for(;p.length;)p.shift()()})}]).controller("UibDaypickerController",["$scope","$element","dateFilter",function(a,b,c){function d(a,b){return 1!==b||a%4!==0||a%100===0&&a%400!==0?f[b]:29}function e(a){var b=new Date(a);b.setDate(b.getDate()+4-(b.getDay()||7));var c=b.getTime();return b.setMonth(0),b.setDate(1),Math.floor(Math.round((c-b)/864e5)/7)+1}var f=[31,28,31,30,31,30,31,31,30,31,30,31];this.step={months:1},this.element=b,this.init=function(b){angular.extend(b,this),a.showWeeks=b.showWeeks,b.refreshView()},this.getDates=function(a,b){for(var c,d=new Array(b),e=new Date(a),f=0;b>f;)c=new Date(e),d[f++]=c,e.setDate(e.getDate()+1);return d},this._refreshView=function(){var b=this.activeDate.getFullYear(),d=this.activeDate.getMonth(),f=new Date(this.activeDate);f.setFullYear(b,d,1);var g=this.startingDay-f.getDay(),h=g>0?7-g:-g,i=new Date(f);h>0&&i.setDate(-h+1);for(var j=this.getDates(i,42),k=0;42>k;k++)j[k]=angular.extend(this.createDateObject(j[k],this.formatDay),{secondary:j[k].getMonth()!==d,uid:a.uniqueId+"-"+k});a.labels=new Array(7);for(var l=0;7>l;l++)a.labels[l]={abbr:c(j[l].date,this.formatDayHeader),full:c(j[l].date,"EEEE")};if(a.title=c(this.activeDate,this.formatDayTitle),a.rows=this.split(j,7),a.showWeeks){a.weekNumbers=[];for(var m=(11-this.startingDay)%7,n=a.rows.length,o=0;n>o;o++)a.weekNumbers.push(e(a.rows[o][m].date))}},this.compare=function(a,b){var c=new Date(a.getFullYear(),a.getMonth(),a.getDate()),d=new Date(b.getFullYear(),b.getMonth(),b.getDate());return c.setFullYear(a.getFullYear()),d.setFullYear(b.getFullYear()),c-d},this.handleKeyDown=function(a,b){var c=this.activeDate.getDate();if("left"===a)c-=1;else if("up"===a)c-=7;else if("right"===a)c+=1;else if("down"===a)c+=7;else if("pageup"===a||"pagedown"===a){var e=this.activeDate.getMonth()+("pageup"===a?-1:1);this.activeDate.setMonth(e,1),c=Math.min(d(this.activeDate.getFullYear(),this.activeDate.getMonth()),c)}else"home"===a?c=1:"end"===a&&(c=d(this.activeDate.getFullYear(),this.activeDate.getMonth()));this.activeDate.setDate(c)}}]).controller("UibMonthpickerController",["$scope","$element","dateFilter",function(a,b,c){this.step={years:1},this.element=b,this.init=function(a){angular.extend(a,this),a.refreshView()},this._refreshView=function(){for(var b,d=new Array(12),e=this.activeDate.getFullYear(),f=0;12>f;f++)b=new Date(this.activeDate),b.setFullYear(e,f,1),d[f]=angular.extend(this.createDateObject(b,this.formatMonth),{uid:a.uniqueId+"-"+f});a.title=c(this.activeDate,this.formatMonthTitle),a.rows=this.split(d,3)},this.compare=function(a,b){var c=new Date(a.getFullYear(),a.getMonth()),d=new Date(b.getFullYear(),b.getMonth());return c.setFullYear(a.getFullYear()),d.setFullYear(b.getFullYear()),c-d},this.handleKeyDown=function(a,b){var c=this.activeDate.getMonth();if("left"===a)c-=1;else if("up"===a)c-=3;else if("right"===a)c+=1;else if("down"===a)c+=3;else if("pageup"===a||"pagedown"===a){var d=this.activeDate.getFullYear()+("pageup"===a?-1:1);this.activeDate.setFullYear(d)}else"home"===a?c=0:"end"===a&&(c=11);this.activeDate.setMonth(c)}}]).controller("UibYearpickerController",["$scope","$element","dateFilter",function(a,b,c){function d(a){return parseInt((a-1)/f,10)*f+1}var e,f;this.element=b,this.yearpickerInit=function(){e=this.yearColumns,f=this.yearRows*e,this.step={years:f}},this._refreshView=function(){for(var b,c=new Array(f),g=0,h=d(this.activeDate.getFullYear());f>g;g++)b=new Date(this.activeDate),b.setFullYear(h+g,0,1),c[g]=angular.extend(this.createDateObject(b,this.formatYear),{uid:a.uniqueId+"-"+g});a.title=[c[0].label,c[f-1].label].join(" - "),a.rows=this.split(c,e),a.columns=e},this.compare=function(a,b){return a.getFullYear()-b.getFullYear()},this.handleKeyDown=function(a,b){var c=this.activeDate.getFullYear();"left"===a?c-=1:"up"===a?c-=e:"right"===a?c+=1:"down"===a?c+=e:"pageup"===a||"pagedown"===a?c+=("pageup"===a?-1:1)*f:"home"===a?c=d(this.activeDate.getFullYear()):"end"===a&&(c=d(this.activeDate.getFullYear())+f-1),this.activeDate.setFullYear(c)}}]).directive("uibDatepicker",function(){return{replace:!0,templateUrl:function(a,b){return b.templateUrl||"uib/template/datepicker/datepicker.html"},scope:{datepickerOptions:"=?"},require:["uibDatepicker","^ngModel"],controller:"UibDatepickerController",controllerAs:"datepicker",link:function(a,b,c,d){var e=d[0],f=d[1];e.init(f)}}}).directive("uibDaypicker",function(){return{replace:!0,templateUrl:function(a,b){return b.templateUrl||"uib/template/datepicker/day.html"},require:["^uibDatepicker","uibDaypicker"],controller:"UibDaypickerController",link:function(a,b,c,d){var e=d[0],f=d[1];f.init(e)}}}).directive("uibMonthpicker",function(){return{replace:!0,templateUrl:function(a,b){return b.templateUrl||"uib/template/datepicker/month.html"},require:["^uibDatepicker","uibMonthpicker"],controller:"UibMonthpickerController",link:function(a,b,c,d){var e=d[0],f=d[1];f.init(e)}}}).directive("uibYearpicker",function(){return{replace:!0,templateUrl:function(a,b){return b.templateUrl||"uib/template/datepicker/year.html"},require:["^uibDatepicker","uibYearpicker"],controller:"UibYearpickerController",link:function(a,b,c,d){var e=d[0];angular.extend(e,d[1]),e.yearpickerInit(),e.refreshView()}}}),angular.module("ui.bootstrap.position",[]).factory("$uibPosition",["$document","$window",function(a,b){var c,d,e={normal:/(auto|scroll)/,hidden:/(auto|scroll|hidden)/},f={auto:/\s?auto?\s?/i,primary:/^(top|bottom|left|right)$/,secondary:/^(top|bottom|left|right|center)$/,vertical:/^(top|bottom)$/},g=/(HTML|BODY)/;return{getRawNode:function(a){return a.nodeName?a:a[0]||a},parseStyle:function(a){return a=parseFloat(a),isFinite(a)?a:0},offsetParent:function(c){function d(a){return"static"===(b.getComputedStyle(a).position||"static")}c=this.getRawNode(c);for(var e=c.offsetParent||a[0].documentElement;e&&e!==a[0].documentElement&&d(e);)e=e.offsetParent;return e||a[0].documentElement},scrollbarWidth:function(e){if(e){if(angular.isUndefined(d)){var f=a.find("body");f.addClass("uib-position-body-scrollbar-measure"),d=b.innerWidth-f[0].clientWidth,d=isFinite(d)?d:0,f.removeClass("uib-position-body-scrollbar-measure")}return d}if(angular.isUndefined(c)){var g=angular.element('<div class="uib-position-scrollbar-measure"></div>');a.find("body").append(g),c=g[0].offsetWidth-g[0].clientWidth,c=isFinite(c)?c:0,g.remove()}return c},scrollbarPadding:function(a){a=this.getRawNode(a);var c=b.getComputedStyle(a),d=this.parseStyle(c.paddingRight),e=this.parseStyle(c.paddingBottom),f=this.scrollParent(a,!1,!0),h=this.scrollbarWidth(f,g.test(f.tagName));return{scrollbarWidth:h,widthOverflow:f.scrollWidth>f.clientWidth,right:d+h,originalRight:d,heightOverflow:f.scrollHeight>f.clientHeight,
bottom:e+h,originalBottom:e}},isScrollable:function(a,c){a=this.getRawNode(a);var d=c?e.hidden:e.normal,f=b.getComputedStyle(a);return d.test(f.overflow+f.overflowY+f.overflowX)},scrollParent:function(c,d,f){c=this.getRawNode(c);var g=d?e.hidden:e.normal,h=a[0].documentElement,i=b.getComputedStyle(c);if(f&&g.test(i.overflow+i.overflowY+i.overflowX))return c;var j="absolute"===i.position,k=c.parentElement||h;if(k===h||"fixed"===i.position)return h;for(;k.parentElement&&k!==h;){var l=b.getComputedStyle(k);if(j&&"static"!==l.position&&(j=!1),!j&&g.test(l.overflow+l.overflowY+l.overflowX))break;k=k.parentElement}return k},position:function(c,d){c=this.getRawNode(c);var e=this.offset(c);if(d){var f=b.getComputedStyle(c);e.top-=this.parseStyle(f.marginTop),e.left-=this.parseStyle(f.marginLeft)}var g=this.offsetParent(c),h={top:0,left:0};return g!==a[0].documentElement&&(h=this.offset(g),h.top+=g.clientTop-g.scrollTop,h.left+=g.clientLeft-g.scrollLeft),{width:Math.round(angular.isNumber(e.width)?e.width:c.offsetWidth),height:Math.round(angular.isNumber(e.height)?e.height:c.offsetHeight),top:Math.round(e.top-h.top),left:Math.round(e.left-h.left)}},offset:function(c){c=this.getRawNode(c);var d=c.getBoundingClientRect();return{width:Math.round(angular.isNumber(d.width)?d.width:c.offsetWidth),height:Math.round(angular.isNumber(d.height)?d.height:c.offsetHeight),top:Math.round(d.top+(b.pageYOffset||a[0].documentElement.scrollTop)),left:Math.round(d.left+(b.pageXOffset||a[0].documentElement.scrollLeft))}},viewportOffset:function(c,d,e){c=this.getRawNode(c),e=e!==!1;var f=c.getBoundingClientRect(),g={top:0,left:0,bottom:0,right:0},h=d?a[0].documentElement:this.scrollParent(c),i=h.getBoundingClientRect();if(g.top=i.top+h.clientTop,g.left=i.left+h.clientLeft,h===a[0].documentElement&&(g.top+=b.pageYOffset,g.left+=b.pageXOffset),g.bottom=g.top+h.clientHeight,g.right=g.left+h.clientWidth,e){var j=b.getComputedStyle(h);g.top+=this.parseStyle(j.paddingTop),g.bottom-=this.parseStyle(j.paddingBottom),g.left+=this.parseStyle(j.paddingLeft),g.right-=this.parseStyle(j.paddingRight)}return{top:Math.round(f.top-g.top),bottom:Math.round(g.bottom-f.bottom),left:Math.round(f.left-g.left),right:Math.round(g.right-f.right)}},parsePlacement:function(a){var b=f.auto.test(a);return b&&(a=a.replace(f.auto,"")),a=a.split("-"),a[0]=a[0]||"top",f.primary.test(a[0])||(a[0]="top"),a[1]=a[1]||"center",f.secondary.test(a[1])||(a[1]="center"),b?a[2]=!0:a[2]=!1,a},positionElements:function(a,c,d,e){a=this.getRawNode(a),c=this.getRawNode(c);var g=angular.isDefined(c.offsetWidth)?c.offsetWidth:c.prop("offsetWidth"),h=angular.isDefined(c.offsetHeight)?c.offsetHeight:c.prop("offsetHeight");d=this.parsePlacement(d);var i=e?this.offset(a):this.position(a),j={top:0,left:0,placement:""};if(d[2]){var k=this.viewportOffset(a,e),l=b.getComputedStyle(c),m={width:g+Math.round(Math.abs(this.parseStyle(l.marginLeft)+this.parseStyle(l.marginRight))),height:h+Math.round(Math.abs(this.parseStyle(l.marginTop)+this.parseStyle(l.marginBottom)))};if(d[0]="top"===d[0]&&m.height>k.top&&m.height<=k.bottom?"bottom":"bottom"===d[0]&&m.height>k.bottom&&m.height<=k.top?"top":"left"===d[0]&&m.width>k.left&&m.width<=k.right?"right":"right"===d[0]&&m.width>k.right&&m.width<=k.left?"left":d[0],d[1]="top"===d[1]&&m.height-i.height>k.bottom&&m.height-i.height<=k.top?"bottom":"bottom"===d[1]&&m.height-i.height>k.top&&m.height-i.height<=k.bottom?"top":"left"===d[1]&&m.width-i.width>k.right&&m.width-i.width<=k.left?"right":"right"===d[1]&&m.width-i.width>k.left&&m.width-i.width<=k.right?"left":d[1],"center"===d[1])if(f.vertical.test(d[0])){var n=i.width/2-g/2;k.left+n<0&&m.width-i.width<=k.right?d[1]="left":k.right+n<0&&m.width-i.width<=k.left&&(d[1]="right")}else{var o=i.height/2-m.height/2;k.top+o<0&&m.height-i.height<=k.bottom?d[1]="top":k.bottom+o<0&&m.height-i.height<=k.top&&(d[1]="bottom")}}switch(d[0]){case"top":j.top=i.top-h;break;case"bottom":j.top=i.top+i.height;break;case"left":j.left=i.left-g;break;case"right":j.left=i.left+i.width}switch(d[1]){case"top":j.top=i.top;break;case"bottom":j.top=i.top+i.height-h;break;case"left":j.left=i.left;break;case"right":j.left=i.left+i.width-g;break;case"center":f.vertical.test(d[0])?j.left=i.left+i.width/2-g/2:j.top=i.top+i.height/2-h/2}return j.top=Math.round(j.top),j.left=Math.round(j.left),j.placement="center"===d[1]?d[0]:d[0]+"-"+d[1],j},positionArrow:function(a,c){a=this.getRawNode(a);var d=a.querySelector(".tooltip-inner, .popover-inner");if(d){var e=angular.element(d).hasClass("tooltip-inner"),g=e?a.querySelector(".tooltip-arrow"):a.querySelector(".arrow");if(g){var h={top:"",bottom:"",left:"",right:""};if(c=this.parsePlacement(c),"center"===c[1])return void angular.element(g).css(h);var i="border-"+c[0]+"-width",j=b.getComputedStyle(g)[i],k="border-";k+=f.vertical.test(c[0])?c[0]+"-"+c[1]:c[1]+"-"+c[0],k+="-radius";var l=b.getComputedStyle(e?d:a)[k];switch(c[0]){case"top":h.bottom=e?"0":"-"+j;break;case"bottom":h.top=e?"0":"-"+j;break;case"left":h.right=e?"0":"-"+j;break;case"right":h.left=e?"0":"-"+j}h[c[1]]=l,angular.element(g).css(h)}}}}}]),angular.module("ui.bootstrap.datepickerPopup",["ui.bootstrap.datepicker","ui.bootstrap.position"]).value("$datepickerPopupLiteralWarning",!0).constant("uibDatepickerPopupConfig",{altInputFormats:[],appendToBody:!1,clearText:"Clear",closeOnDateSelection:!0,closeText:"Done",currentText:"Today",datepickerPopup:"yyyy-MM-dd",datepickerPopupTemplateUrl:"uib/template/datepickerPopup/popup.html",datepickerTemplateUrl:"uib/template/datepicker/datepicker.html",html5Types:{date:"yyyy-MM-dd","datetime-local":"yyyy-MM-ddTHH:mm:ss.sss",month:"yyyy-MM"},onOpenFocus:!0,showButtonBar:!0,placement:"auto bottom-left"}).controller("UibDatepickerPopupController",["$scope","$element","$attrs","$compile","$log","$parse","$window","$document","$rootScope","$uibPosition","dateFilter","uibDateParser","uibDatepickerPopupConfig","$timeout","uibDatepickerConfig","$datepickerPopupLiteralWarning",function(a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p){function q(b){var c=l.parse(b,w,a.date);if(isNaN(c))for(var d=0;d<I.length;d++)if(c=l.parse(b,I[d],a.date),!isNaN(c))return c;return c}function r(a){if(angular.isNumber(a)&&(a=new Date(a)),!a)return null;if(angular.isDate(a)&&!isNaN(a))return a;if(angular.isString(a)){var b=q(a);if(!isNaN(b))return l.toTimezone(b,J)}return F.$options&&F.$options.allowInvalid?a:void 0}function s(a,b){var d=a||b;return c.ngRequired||d?(angular.isNumber(d)&&(d=new Date(d)),d?angular.isDate(d)&&!isNaN(d)?!0:angular.isString(d)?!isNaN(q(b)):!1:!0):!0}function t(c){if(a.isOpen||!a.disabled){var d=H[0],e=b[0].contains(c.target),f=void 0!==d.contains&&d.contains(c.target);!a.isOpen||e||f||a.$apply(function(){a.isOpen=!1})}}function u(c){27===c.which&&a.isOpen?(c.preventDefault(),c.stopPropagation(),a.$apply(function(){a.isOpen=!1}),b[0].focus()):40!==c.which||a.isOpen||(c.preventDefault(),c.stopPropagation(),a.$apply(function(){a.isOpen=!0}))}function v(){if(a.isOpen){var d=angular.element(H[0].querySelector(".uib-datepicker-popup")),e=c.popupPlacement?c.popupPlacement:m.placement,f=j.positionElements(b,d,e,y);d.css({top:f.top+"px",left:f.left+"px"}),d.hasClass("uib-position-measure")&&d.removeClass("uib-position-measure")}}var w,x,y,z,A,B,C,D,E,F,G,H,I,J,K=!1,L=[];this.init=function(e){if(F=e,G=e.$options,x=angular.isDefined(c.closeOnDateSelection)?a.$parent.$eval(c.closeOnDateSelection):m.closeOnDateSelection,y=angular.isDefined(c.datepickerAppendToBody)?a.$parent.$eval(c.datepickerAppendToBody):m.appendToBody,z=angular.isDefined(c.onOpenFocus)?a.$parent.$eval(c.onOpenFocus):m.onOpenFocus,A=angular.isDefined(c.datepickerPopupTemplateUrl)?c.datepickerPopupTemplateUrl:m.datepickerPopupTemplateUrl,B=angular.isDefined(c.datepickerTemplateUrl)?c.datepickerTemplateUrl:m.datepickerTemplateUrl,I=angular.isDefined(c.altInputFormats)?a.$parent.$eval(c.altInputFormats):m.altInputFormats,a.showButtonBar=angular.isDefined(c.showButtonBar)?a.$parent.$eval(c.showButtonBar):m.showButtonBar,m.html5Types[c.type]?(w=m.html5Types[c.type],K=!0):(w=c.uibDatepickerPopup||m.datepickerPopup,c.$observe("uibDatepickerPopup",function(a,b){var c=a||m.datepickerPopup;if(c!==w&&(w=c,F.$modelValue=null,!w))throw new Error("uibDatepickerPopup must have a date format specified.")})),!w)throw new Error("uibDatepickerPopup must have a date format specified.");if(K&&c.uibDatepickerPopup)throw new Error("HTML5 date input types do not support custom formats.");C=angular.element("<div uib-datepicker-popup-wrap><div uib-datepicker></div></div>"),G?(J=G.timezone,a.ngModelOptions=angular.copy(G),a.ngModelOptions.timezone=null,a.ngModelOptions.updateOnDefault===!0&&(a.ngModelOptions.updateOn=a.ngModelOptions.updateOn?a.ngModelOptions.updateOn+" default":"default"),C.attr("ng-model-options","ngModelOptions")):J=null,C.attr({"ng-model":"date","ng-change":"dateSelection(date)","template-url":A}),D=angular.element(C.children()[0]),D.attr("template-url",B),a.datepickerOptions||(a.datepickerOptions={}),K&&"month"===c.type&&(a.datepickerOptions.datepickerMode="month",a.datepickerOptions.minMode="month"),D.attr("datepicker-options","datepickerOptions"),K?F.$formatters.push(function(b){return a.date=l.fromTimezone(b,J),b}):(F.$$parserName="date",F.$validators.date=s,F.$parsers.unshift(r),F.$formatters.push(function(b){return F.$isEmpty(b)?(a.date=b,b):(angular.isNumber(b)&&(b=new Date(b)),a.date=l.fromTimezone(b,J),l.filter(a.date,w))})),F.$viewChangeListeners.push(function(){a.date=q(F.$viewValue)}),b.on("keydown",u),H=d(C)(a),C.remove(),y?h.find("body").append(H):b.after(H),a.$on("$destroy",function(){for(a.isOpen===!0&&(i.$$phase||a.$apply(function(){a.isOpen=!1})),H.remove(),b.off("keydown",u),h.off("click",t),E&&E.off("scroll",v),angular.element(g).off("resize",v);L.length;)L.shift()()})},a.getText=function(b){return a[b+"Text"]||m[b+"Text"]},a.isDisabled=function(b){"today"===b&&(b=l.fromTimezone(new Date,J));var c={};return angular.forEach(["minDate","maxDate"],function(b){a.datepickerOptions[b]?angular.isDate(a.datepickerOptions[b])?c[b]=l.fromTimezone(new Date(a.datepickerOptions[b]),J):(p&&e.warn("Literal date support has been deprecated, please switch to date object usage"),c[b]=new Date(k(a.datepickerOptions[b],"medium"))):c[b]=null}),a.datepickerOptions&&c.minDate&&a.compare(b,c.minDate)<0||c.maxDate&&a.compare(b,c.maxDate)>0},a.compare=function(a,b){return new Date(a.getFullYear(),a.getMonth(),a.getDate())-new Date(b.getFullYear(),b.getMonth(),b.getDate())},a.dateSelection=function(c){angular.isDefined(c)&&(a.date=c);var d=a.date?l.filter(a.date,w):null;b.val(d),F.$setViewValue(d),x&&(a.isOpen=!1,b[0].focus())},a.keydown=function(c){27===c.which&&(c.stopPropagation(),a.isOpen=!1,b[0].focus())},a.select=function(b,c){if(c.stopPropagation(),"today"===b){var d=new Date;angular.isDate(a.date)?(b=new Date(a.date),b.setFullYear(d.getFullYear(),d.getMonth(),d.getDate())):b=new Date(d.setHours(0,0,0,0))}a.dateSelection(b)},a.close=function(c){c.stopPropagation(),a.isOpen=!1,b[0].focus()},a.disabled=angular.isDefined(c.disabled)||!1,c.ngDisabled&&L.push(a.$parent.$watch(f(c.ngDisabled),function(b){a.disabled=b})),a.$watch("isOpen",function(d){d?a.disabled?a.isOpen=!1:n(function(){v(),z&&a.$broadcast("uib:datepicker.focus"),h.on("click",t);var d=c.popupPlacement?c.popupPlacement:m.placement;y||j.parsePlacement(d)[2]?(E=E||angular.element(j.scrollParent(b)),E&&E.on("scroll",v)):E=null,angular.element(g).on("resize",v)},0,!1):(h.off("click",t),E&&E.off("scroll",v),angular.element(g).off("resize",v))}),a.$on("uib:datepicker.mode",function(){n(v,0,!1)})}]).directive("uibDatepickerPopup",function(){return{require:["ngModel","uibDatepickerPopup"],controller:"UibDatepickerPopupController",scope:{datepickerOptions:"=?",isOpen:"=?",currentText:"@",clearText:"@",closeText:"@"},link:function(a,b,c,d){var e=d[0],f=d[1];f.init(e)}}}).directive("uibDatepickerPopupWrap",function(){return{replace:!0,transclude:!0,templateUrl:function(a,b){return b.templateUrl||"uib/template/datepickerPopup/popup.html"}}}),angular.module("ui.bootstrap.debounce",[]).factory("$$debounce",["$timeout",function(a){return function(b,c){var d;return function(){var e=this,f=Array.prototype.slice.call(arguments);d&&a.cancel(d),d=a(function(){b.apply(e,f)},c)}}}]),angular.module("ui.bootstrap.dropdown",["ui.bootstrap.position"]).constant("uibDropdownConfig",{appendToOpenClass:"uib-dropdown-open",openClass:"open"}).service("uibDropdownService",["$document","$rootScope",function(a,b){var c=null;this.open=function(b,f){c||(a.on("click",d),f.on("keydown",e)),c&&c!==b&&(c.isOpen=!1),c=b},this.close=function(b,f){c===b&&(c=null,a.off("click",d),f.off("keydown",e))};var d=function(a){if(c&&!(a&&"disabled"===c.getAutoClose()||a&&3===a.which)){var d=c.getToggleElement();if(!(a&&d&&d[0].contains(a.target))){var e=c.getDropdownElement();a&&"outsideClick"===c.getAutoClose()&&e&&e[0].contains(a.target)||(c.isOpen=!1,b.$$phase||c.$apply())}}},e=function(a){27===a.which?(a.stopPropagation(),c.focusToggleElement(),d()):c.isKeynavEnabled()&&-1!==[38,40].indexOf(a.which)&&c.isOpen&&(a.preventDefault(),a.stopPropagation(),c.focusDropdownEntry(a.which))}}]).controller("UibDropdownController",["$scope","$element","$attrs","$parse","uibDropdownConfig","uibDropdownService","$animate","$uibPosition","$document","$compile","$templateRequest",function(a,b,c,d,e,f,g,h,i,j,k){var l,m,n=this,o=a.$new(),p=e.appendToOpenClass,q=e.openClass,r=angular.noop,s=c.onToggle?d(c.onToggle):angular.noop,t=!1,u=null,v=!1,w=i.find("body");b.addClass("dropdown"),this.init=function(){if(c.isOpen&&(m=d(c.isOpen),r=m.assign,a.$watch(m,function(a){o.isOpen=!!a})),angular.isDefined(c.dropdownAppendTo)){var e=d(c.dropdownAppendTo)(o);e&&(u=angular.element(e))}t=angular.isDefined(c.dropdownAppendToBody),v=angular.isDefined(c.keyboardNav),t&&!u&&(u=w),u&&n.dropdownMenu&&(u.append(n.dropdownMenu),b.on("$destroy",function(){n.dropdownMenu.remove()}))},this.toggle=function(a){return o.isOpen=arguments.length?!!a:!o.isOpen,angular.isFunction(r)&&r(o,o.isOpen),o.isOpen},this.isOpen=function(){return o.isOpen},o.getToggleElement=function(){return n.toggleElement},o.getAutoClose=function(){return c.autoClose||"always"},o.getElement=function(){return b},o.isKeynavEnabled=function(){return v},o.focusDropdownEntry=function(a){var c=n.dropdownMenu?angular.element(n.dropdownMenu).find("a"):b.find("ul").eq(0).find("a");switch(a){case 40:angular.isNumber(n.selectedOption)?n.selectedOption=n.selectedOption===c.length-1?n.selectedOption:n.selectedOption+1:n.selectedOption=0;break;case 38:angular.isNumber(n.selectedOption)?n.selectedOption=0===n.selectedOption?0:n.selectedOption-1:n.selectedOption=c.length-1}c[n.selectedOption].focus()},o.getDropdownElement=function(){return n.dropdownMenu},o.focusToggleElement=function(){n.toggleElement&&n.toggleElement[0].focus()},o.$watch("isOpen",function(c,d){if(u&&n.dropdownMenu){var e,i,m,v=h.positionElements(b,n.dropdownMenu,"bottom-left",!0);if(e={top:v.top+"px",display:c?"block":"none"},i=n.dropdownMenu.hasClass("dropdown-menu-right"),i?(e.left="auto",m=h.scrollbarWidth(!0),e.right=window.innerWidth-m-(v.left+b.prop("offsetWidth"))+"px"):(e.left=v.left+"px",e.right="auto"),!t){var w=h.offset(u);e.top=v.top-w.top+"px",i?e.right=window.innerWidth-(v.left-w.left+b.prop("offsetWidth"))+"px":e.left=v.left-w.left+"px"}n.dropdownMenu.css(e)}var x=u?u:b,y=x.hasClass(u?p:q);if(y===!c&&g[c?"addClass":"removeClass"](x,u?p:q).then(function(){angular.isDefined(c)&&c!==d&&s(a,{open:!!c})}),c)n.dropdownMenuTemplateUrl&&k(n.dropdownMenuTemplateUrl).then(function(a){l=o.$new(),j(a.trim())(l,function(a){var b=a;n.dropdownMenu.replaceWith(b),n.dropdownMenu=b})}),o.focusToggleElement(),f.open(o,b);else{if(n.dropdownMenuTemplateUrl){l&&l.$destroy();var z=angular.element('<ul class="dropdown-menu"></ul>');n.dropdownMenu.replaceWith(z),n.dropdownMenu=z}f.close(o,b),n.selectedOption=null}angular.isFunction(r)&&r(a,c)})}]).directive("uibDropdown",function(){return{controller:"UibDropdownController",link:function(a,b,c,d){d.init()}}}).directive("uibDropdownMenu",function(){return{restrict:"A",require:"?^uibDropdown",link:function(a,b,c,d){if(d&&!angular.isDefined(c.dropdownNested)){b.addClass("dropdown-menu");var e=c.templateUrl;e&&(d.dropdownMenuTemplateUrl=e),d.dropdownMenu||(d.dropdownMenu=b)}}}}).directive("uibDropdownToggle",function(){return{require:"?^uibDropdown",link:function(a,b,c,d){if(d){b.addClass("dropdown-toggle"),d.toggleElement=b;var e=function(e){e.preventDefault(),b.hasClass("disabled")||c.disabled||a.$apply(function(){d.toggle()})};b.bind("click",e),b.attr({"aria-haspopup":!0,"aria-expanded":!1}),a.$watch(d.isOpen,function(a){b.attr("aria-expanded",!!a)}),a.$on("$destroy",function(){b.unbind("click",e)})}}}}),angular.module("ui.bootstrap.stackedMap",[]).factory("$$stackedMap",function(){return{createNew:function(){var a=[];return{add:function(b,c){a.push({key:b,value:c})},get:function(b){for(var c=0;c<a.length;c++)if(b===a[c].key)return a[c]},keys:function(){for(var b=[],c=0;c<a.length;c++)b.push(a[c].key);return b},top:function(){return a[a.length-1]},remove:function(b){for(var c=-1,d=0;d<a.length;d++)if(b===a[d].key){c=d;break}return a.splice(c,1)[0]},removeTop:function(){return a.splice(a.length-1,1)[0]},length:function(){return a.length}}}}}),angular.module("ui.bootstrap.modal",["ui.bootstrap.stackedMap","ui.bootstrap.position"]).factory("$$multiMap",function(){return{createNew:function(){var a={};return{entries:function(){return Object.keys(a).map(function(b){return{key:b,value:a[b]}})},get:function(b){return a[b]},hasKey:function(b){return!!a[b]},keys:function(){return Object.keys(a)},put:function(b,c){a[b]||(a[b]=[]),a[b].push(c)},remove:function(b,c){var d=a[b];if(d){var e=d.indexOf(c);-1!==e&&d.splice(e,1),d.length||delete a[b]}}}}}}).provider("$uibResolve",function(){var a=this;this.resolver=null,this.setResolver=function(a){this.resolver=a},this.$get=["$injector","$q",function(b,c){var d=a.resolver?b.get(a.resolver):null;return{resolve:function(a,e,f,g){if(d)return d.resolve(a,e,f,g);var h=[];return angular.forEach(a,function(a){angular.isFunction(a)||angular.isArray(a)?h.push(c.resolve(b.invoke(a))):angular.isString(a)?h.push(c.resolve(b.get(a))):h.push(c.resolve(a))}),c.all(h).then(function(b){var c={},d=0;return angular.forEach(a,function(a,e){c[e]=b[d++]}),c})}}}]}).directive("uibModalBackdrop",["$animate","$injector","$uibModalStack",function(a,b,c){function d(b,d,e){e.modalInClass&&(a.addClass(d,e.modalInClass),b.$on(c.NOW_CLOSING_EVENT,function(c,f){var g=f();b.modalOptions.animation?a.removeClass(d,e.modalInClass).then(g):g()}))}return{replace:!0,templateUrl:"uib/template/modal/backdrop.html",compile:function(a,b){return a.addClass(b.backdropClass),d}}}]).directive("uibModalWindow",["$uibModalStack","$q","$animateCss","$document",function(a,b,c,d){return{scope:{index:"@"},replace:!0,transclude:!0,templateUrl:function(a,b){return b.templateUrl||"uib/template/modal/window.html"},link:function(e,f,g){f.addClass(g.windowClass||""),f.addClass(g.windowTopClass||""),e.size=g.size,e.close=function(b){var c=a.getTop();c&&c.value.backdrop&&"static"!==c.value.backdrop&&b.target===b.currentTarget&&(b.preventDefault(),b.stopPropagation(),a.dismiss(c.key,"backdrop click"))},f.on("click",e.close),e.$isRendered=!0;var h=b.defer();g.$observe("modalRender",function(a){"true"===a&&h.resolve()}),h.promise.then(function(){var h=null;g.modalInClass&&(h=c(f,{addClass:g.modalInClass}).start(),e.$on(a.NOW_CLOSING_EVENT,function(a,b){var d=b();c(f,{removeClass:g.modalInClass}).start().then(d)})),b.when(h).then(function(){var b=a.getTop();if(b&&a.modalRendered(b.key),!d[0].activeElement||!f[0].contains(d[0].activeElement)){var c=f[0].querySelector("[autofocus]");c?c.focus():f[0].focus()}})})}}}]).directive("uibModalAnimationClass",function(){return{compile:function(a,b){b.modalAnimation&&a.addClass(b.uibModalAnimationClass)}}}).directive("uibModalTransclude",function(){return{link:function(a,b,c,d,e){e(a.$parent,function(a){b.empty(),b.append(a)})}}}).factory("$uibModalStack",["$animate","$animateCss","$document","$compile","$rootScope","$q","$$multiMap","$$stackedMap","$uibPosition",function(a,b,c,d,e,f,g,h,i){function j(a){return!!(a.offsetWidth||a.offsetHeight||a.getClientRects().length)}function k(){for(var a=-1,b=v.keys(),c=0;c<b.length;c++)v.get(b[c]).value.backdrop&&(a=c);return a>-1&&y>a&&(a=y),a}function l(a,b){var c=v.get(a).value,d=c.appendTo;v.remove(a),z=v.top(),z&&(y=parseInt(z.value.modalDomEl.attr("index"),10)),o(c.modalDomEl,c.modalScope,function(){var b=c.openedClass||u;w.remove(b,a);var e=w.hasKey(b);d.toggleClass(b,e),!e&&t&&t.heightOverflow&&t.scrollbarWidth&&(t.originalRight?d.css({paddingRight:t.originalRight+"px"}):d.css({paddingRight:""}),t=null),m(!0)},c.closedDeferred),n(),b&&b.focus?b.focus():d.focus&&d.focus()}function m(a){var b;v.length()>0&&(b=v.top().value,b.modalDomEl.toggleClass(b.windowTopClass||"",a))}function n(){if(r&&-1===k()){var a=s;o(r,s,function(){a=null}),r=void 0,s=void 0}}function o(b,c,d,e){function g(){g.done||(g.done=!0,a.leave(b).then(function(){b.remove(),e&&e.resolve()}),c.$destroy(),d&&d())}var h,i=null,j=function(){return h||(h=f.defer(),i=h.promise),function(){h.resolve()}};return c.$broadcast(x.NOW_CLOSING_EVENT,j),f.when(i).then(g)}function p(a){if(a.isDefaultPrevented())return a;var b=v.top();if(b)switch(a.which){case 27:b.value.keyboard&&(a.preventDefault(),e.$apply(function(){x.dismiss(b.key,"escape key press")}));break;case 9:var c=x.loadFocusElementList(b),d=!1;a.shiftKey?(x.isFocusInFirstItem(a,c)||x.isModalFocused(a,b))&&(d=x.focusLastFocusableElement(c)):x.isFocusInLastItem(a,c)&&(d=x.focusFirstFocusableElement(c)),d&&(a.preventDefault(),a.stopPropagation())}}function q(a,b,c){return!a.value.modalScope.$broadcast("modal.closing",b,c).defaultPrevented}var r,s,t,u="modal-open",v=h.createNew(),w=g.createNew(),x={NOW_CLOSING_EVENT:"modal.stack.now-closing"},y=0,z=null,A="a[href], area[href], input:not([disabled]), button:not([disabled]),select:not([disabled]), textarea:not([disabled]), iframe, object, embed, *[tabindex], *[contenteditable=true]";return e.$watch(k,function(a){s&&(s.index=a)}),c.on("keydown",p),e.$on("$destroy",function(){c.off("keydown",p)}),x.open=function(b,f){var g=c[0].activeElement,h=f.openedClass||u;m(!1),z=v.top(),v.add(b,{deferred:f.deferred,renderDeferred:f.renderDeferred,closedDeferred:f.closedDeferred,modalScope:f.scope,backdrop:f.backdrop,keyboard:f.keyboard,openedClass:f.openedClass,windowTopClass:f.windowTopClass,animation:f.animation,appendTo:f.appendTo}),w.put(h,b);var j=f.appendTo,l=k();if(!j.length)throw new Error("appendTo element not found. Make sure that the element passed is in DOM.");l>=0&&!r&&(s=e.$new(!0),s.modalOptions=f,s.index=l,r=angular.element('<div uib-modal-backdrop="modal-backdrop"></div>'),r.attr("backdrop-class",f.backdropClass),f.animation&&r.attr("modal-animation","true"),d(r)(s),a.enter(r,j),t=i.scrollbarPadding(j),t.heightOverflow&&t.scrollbarWidth&&j.css({paddingRight:t.right+"px"})),y=z?parseInt(z.value.modalDomEl.attr("index"),10)+1:0;var n=angular.element('<div uib-modal-window="modal-window"></div>');n.attr({"template-url":f.windowTemplateUrl,"window-class":f.windowClass,"window-top-class":f.windowTopClass,size:f.size,index:y,animate:"animate"}).html(f.content),f.animation&&n.attr("modal-animation","true"),j.addClass(h),a.enter(d(n)(f.scope),j),v.top().value.modalDomEl=n,v.top().value.modalOpener=g},x.close=function(a,b){var c=v.get(a);return c&&q(c,b,!0)?(c.value.modalScope.$$uibDestructionScheduled=!0,c.value.deferred.resolve(b),l(a,c.value.modalOpener),!0):!c},x.dismiss=function(a,b){var c=v.get(a);return c&&q(c,b,!1)?(c.value.modalScope.$$uibDestructionScheduled=!0,c.value.deferred.reject(b),l(a,c.value.modalOpener),!0):!c},x.dismissAll=function(a){for(var b=this.getTop();b&&this.dismiss(b.key,a);)b=this.getTop()},x.getTop=function(){return v.top()},x.modalRendered=function(a){var b=v.get(a);b&&b.value.renderDeferred.resolve()},x.focusFirstFocusableElement=function(a){return a.length>0?(a[0].focus(),!0):!1},x.focusLastFocusableElement=function(a){return a.length>0?(a[a.length-1].focus(),!0):!1},x.isModalFocused=function(a,b){if(a&&b){var c=b.value.modalDomEl;if(c&&c.length)return(a.target||a.srcElement)===c[0]}return!1},x.isFocusInFirstItem=function(a,b){return b.length>0?(a.target||a.srcElement)===b[0]:!1},x.isFocusInLastItem=function(a,b){return b.length>0?(a.target||a.srcElement)===b[b.length-1]:!1},x.loadFocusElementList=function(a){if(a){var b=a.value.modalDomEl;if(b&&b.length){var c=b[0].querySelectorAll(A);return c?Array.prototype.filter.call(c,function(a){return j(a)}):c}}},x}]).provider("$uibModal",function(){var a={options:{animation:!0,backdrop:!0,keyboard:!0},$get:["$rootScope","$q","$document","$templateRequest","$controller","$uibResolve","$uibModalStack",function(b,c,d,e,f,g,h){function i(a){return a.template?c.when(a.template):e(angular.isFunction(a.templateUrl)?a.templateUrl():a.templateUrl)}var j={},k=null;return j.getPromiseChain=function(){return k},j.open=function(e){function j(){return r}var l=c.defer(),m=c.defer(),n=c.defer(),o=c.defer(),p={result:l.promise,opened:m.promise,closed:n.promise,rendered:o.promise,close:function(a){return h.close(p,a)},dismiss:function(a){return h.dismiss(p,a)}};if(e=angular.extend({},a.options,e),e.resolve=e.resolve||{},e.appendTo=e.appendTo||d.find("body").eq(0),!e.template&&!e.templateUrl)throw new Error("One of template or templateUrl options is required.");var q,r=c.all([i(e),g.resolve(e.resolve,{},null,null)]);return q=k=c.all([k]).then(j,j).then(function(a){var c=e.scope||b,d=c.$new();d.$close=p.close,d.$dismiss=p.dismiss,d.$on("$destroy",function(){d.$$uibDestructionScheduled||d.$dismiss("$uibUnscheduledDestruction")});var g,i,j={};e.controller&&(j.$scope=d,j.$scope.$resolve={},j.$uibModalInstance=p,angular.forEach(a[1],function(a,b){j[b]=a,j.$scope.$resolve[b]=a}),i=f(e.controller,j,!0,e.controllerAs),e.controllerAs&&e.bindToController&&(g=i.instance,g.$close=d.$close,g.$dismiss=d.$dismiss,angular.extend(g,{$resolve:j.$scope.$resolve},c)),g=i(),angular.isFunction(g.$onInit)&&g.$onInit()),h.open(p,{scope:d,deferred:l,renderDeferred:o,closedDeferred:n,content:a[0],animation:e.animation,backdrop:e.backdrop,keyboard:e.keyboard,backdropClass:e.backdropClass,windowTopClass:e.windowTopClass,windowClass:e.windowClass,windowTemplateUrl:e.windowTemplateUrl,size:e.size,openedClass:e.openedClass,appendTo:e.appendTo}),m.resolve(!0)},function(a){m.reject(a),l.reject(a)})["finally"](function(){k===q&&(k=null)}),p},j}]};return a}),angular.module("ui.bootstrap.paging",[]).factory("uibPaging",["$parse",function(a){return{create:function(b,c,d){b.setNumPages=d.numPages?a(d.numPages).assign:angular.noop,b.ngModelCtrl={$setViewValue:angular.noop},b._watchers=[],b.init=function(a,e){b.ngModelCtrl=a,b.config=e,a.$render=function(){b.render()},d.itemsPerPage?b._watchers.push(c.$parent.$watch(d.itemsPerPage,function(a){b.itemsPerPage=parseInt(a,10),c.totalPages=b.calculateTotalPages(),b.updatePage()})):b.itemsPerPage=e.itemsPerPage,c.$watch("totalItems",function(a,d){(angular.isDefined(a)||a!==d)&&(c.totalPages=b.calculateTotalPages(),b.updatePage())})},b.calculateTotalPages=function(){var a=b.itemsPerPage<1?1:Math.ceil(c.totalItems/b.itemsPerPage);return Math.max(a||0,1)},b.render=function(){c.page=parseInt(b.ngModelCtrl.$viewValue,10)||1},c.selectPage=function(a,d){d&&d.preventDefault();var e=!c.ngDisabled||!d;e&&c.page!==a&&a>0&&a<=c.totalPages&&(d&&d.target&&d.target.blur(),b.ngModelCtrl.$setViewValue(a),b.ngModelCtrl.$render())},c.getText=function(a){return c[a+"Text"]||b.config[a+"Text"]},c.noPrevious=function(){return 1===c.page},c.noNext=function(){return c.page===c.totalPages},b.updatePage=function(){b.setNumPages(c.$parent,c.totalPages),c.page>c.totalPages?c.selectPage(c.totalPages):b.ngModelCtrl.$render()},c.$on("$destroy",function(){for(;b._watchers.length;)b._watchers.shift()()})}}}]),angular.module("ui.bootstrap.pager",["ui.bootstrap.paging"]).controller("UibPagerController",["$scope","$attrs","uibPaging","uibPagerConfig",function(a,b,c,d){a.align=angular.isDefined(b.align)?a.$parent.$eval(b.align):d.align,c.create(this,a,b)}]).constant("uibPagerConfig",{itemsPerPage:10,previousText:"« Previous",nextText:"Next »",align:!0}).directive("uibPager",["uibPagerConfig",function(a){return{scope:{totalItems:"=",previousText:"@",nextText:"@",ngDisabled:"="},require:["uibPager","?ngModel"],controller:"UibPagerController",controllerAs:"pager",templateUrl:function(a,b){return b.templateUrl||"uib/template/pager/pager.html"},replace:!0,link:function(b,c,d,e){var f=e[0],g=e[1];g&&f.init(g,a)}}}]),angular.module("ui.bootstrap.pagination",["ui.bootstrap.paging"]).controller("UibPaginationController",["$scope","$attrs","$parse","uibPaging","uibPaginationConfig",function(a,b,c,d,e){function f(a,b,c){return{number:a,text:b,active:c}}function g(a,b){var c=[],d=1,e=b,g=angular.isDefined(i)&&b>i;g&&(j?(d=Math.max(a-Math.floor(i/2),1),e=d+i-1,e>b&&(e=b,d=e-i+1)):(d=(Math.ceil(a/i)-1)*i+1,e=Math.min(d+i-1,b)));for(var h=d;e>=h;h++){var n=f(h,m(h),h===a);c.push(n)}if(g&&i>0&&(!j||k||l)){if(d>1){if(!l||d>3){var o=f(d-1,"...",!1);c.unshift(o)}if(l){if(3===d){var p=f(2,"2",!1);c.unshift(p)}var q=f(1,"1",!1);c.unshift(q)}}if(b>e){if(!l||b-2>e){var r=f(e+1,"...",!1);c.push(r)}if(l){if(e===b-2){var s=f(b-1,b-1,!1);c.push(s)}var t=f(b,b,!1);c.push(t)}}}return c}var h=this,i=angular.isDefined(b.maxSize)?a.$parent.$eval(b.maxSize):e.maxSize,j=angular.isDefined(b.rotate)?a.$parent.$eval(b.rotate):e.rotate,k=angular.isDefined(b.forceEllipses)?a.$parent.$eval(b.forceEllipses):e.forceEllipses,l=angular.isDefined(b.boundaryLinkNumbers)?a.$parent.$eval(b.boundaryLinkNumbers):e.boundaryLinkNumbers,m=angular.isDefined(b.pageLabel)?function(c){return a.$parent.$eval(b.pageLabel,{$page:c})}:angular.identity;a.boundaryLinks=angular.isDefined(b.boundaryLinks)?a.$parent.$eval(b.boundaryLinks):e.boundaryLinks,a.directionLinks=angular.isDefined(b.directionLinks)?a.$parent.$eval(b.directionLinks):e.directionLinks,d.create(this,a,b),b.maxSize&&h._watchers.push(a.$parent.$watch(c(b.maxSize),function(a){i=parseInt(a,10),h.render()}));var n=this.render;this.render=function(){n(),a.page>0&&a.page<=a.totalPages&&(a.pages=g(a.page,a.totalPages))}}]).constant("uibPaginationConfig",{itemsPerPage:10,boundaryLinks:!1,boundaryLinkNumbers:!1,directionLinks:!0,firstText:"First",previousText:"Previous",nextText:"Next",lastText:"Last",rotate:!0,forceEllipses:!1}).directive("uibPagination",["$parse","uibPaginationConfig",function(a,b){return{scope:{totalItems:"=",firstText:"@",previousText:"@",nextText:"@",lastText:"@",ngDisabled:"="},require:["uibPagination","?ngModel"],controller:"UibPaginationController",controllerAs:"pagination",templateUrl:function(a,b){return b.templateUrl||"uib/template/pagination/pagination.html"},replace:!0,link:function(a,c,d,e){var f=e[0],g=e[1];g&&f.init(g,b)}}}]),angular.module("ui.bootstrap.tooltip",["ui.bootstrap.position","ui.bootstrap.stackedMap"]).provider("$uibTooltip",function(){function a(a){var b=/[A-Z]/g,c="-";return a.replace(b,function(a,b){return(b?c:"")+a.toLowerCase()})}var b={placement:"top",placementClassPrefix:"",animation:!0,popupDelay:0,popupCloseDelay:0,useContentExp:!1},c={mouseenter:"mouseleave",click:"click",outsideClick:"outsideClick",focus:"blur",none:""},d={};this.options=function(a){angular.extend(d,a)},this.setTriggers=function(a){angular.extend(c,a)},this.$get=["$window","$compile","$timeout","$document","$uibPosition","$interpolate","$rootScope","$parse","$$stackedMap",function(e,f,g,h,i,j,k,l,m){function n(a){if(27===a.which){var b=o.top();b&&(b.value.close(),o.removeTop(),b=null)}}var o=m.createNew();return h.on("keypress",n),k.$on("$destroy",function(){h.off("keypress",n)}),function(e,k,m,n){function p(a){var b=(a||n.trigger||m).split(" "),d=b.map(function(a){
return c[a]||a});return{show:b,hide:d}}n=angular.extend({},b,d,n);var q=a(e),r=j.startSymbol(),s=j.endSymbol(),t="<div "+q+'-popup uib-title="'+r+"title"+s+'" '+(n.useContentExp?'content-exp="contentExp()" ':'content="'+r+"content"+s+'" ')+'placement="'+r+"placement"+s+'" popup-class="'+r+"popupClass"+s+'" animation="animation" is-open="isOpen" origin-scope="origScope" class="uib-position-measure"></div>';return{compile:function(a,b){var c=f(t);return function(a,b,d,f){function j(){N.isOpen?q():m()}function m(){M&&!a.$eval(d[k+"Enable"])||(u(),x(),N.popupDelay?G||(G=g(r,N.popupDelay,!1)):r())}function q(){s(),N.popupCloseDelay?H||(H=g(t,N.popupCloseDelay,!1)):t()}function r(){return s(),u(),N.content?(v(),void N.$evalAsync(function(){N.isOpen=!0,y(!0),S()})):angular.noop}function s(){G&&(g.cancel(G),G=null),I&&(g.cancel(I),I=null)}function t(){N&&N.$evalAsync(function(){N&&(N.isOpen=!1,y(!1),N.animation?F||(F=g(w,150,!1)):w())})}function u(){H&&(g.cancel(H),H=null),F&&(g.cancel(F),F=null)}function v(){D||(E=N.$new(),D=c(E,function(a){K?h.find("body").append(a):b.after(a)}),z())}function w(){s(),u(),A(),D&&(D.remove(),D=null),E&&(E.$destroy(),E=null)}function x(){N.title=d[k+"Title"],Q?N.content=Q(a):N.content=d[e],N.popupClass=d[k+"Class"],N.placement=angular.isDefined(d[k+"Placement"])?d[k+"Placement"]:n.placement;var b=i.parsePlacement(N.placement);J=b[1]?b[0]+"-"+b[1]:b[0];var c=parseInt(d[k+"PopupDelay"],10),f=parseInt(d[k+"PopupCloseDelay"],10);N.popupDelay=isNaN(c)?n.popupDelay:c,N.popupCloseDelay=isNaN(f)?n.popupCloseDelay:f}function y(b){P&&angular.isFunction(P.assign)&&P.assign(a,b)}function z(){R.length=0,Q?(R.push(a.$watch(Q,function(a){N.content=a,!a&&N.isOpen&&t()})),R.push(E.$watch(function(){O||(O=!0,E.$$postDigest(function(){O=!1,N&&N.isOpen&&S()}))}))):R.push(d.$observe(e,function(a){N.content=a,!a&&N.isOpen?t():S()})),R.push(d.$observe(k+"Title",function(a){N.title=a,N.isOpen&&S()})),R.push(d.$observe(k+"Placement",function(a){N.placement=a?a:n.placement,N.isOpen&&S()}))}function A(){R.length&&(angular.forEach(R,function(a){a()}),R.length=0)}function B(a){N&&N.isOpen&&D&&(b[0].contains(a.target)||D[0].contains(a.target)||q())}function C(){var a=d[k+"Trigger"];T(),L=p(a),"none"!==L.show&&L.show.forEach(function(a,c){"outsideClick"===a?(b.on("click",j),h.on("click",B)):a===L.hide[c]?b.on(a,j):a&&(b.on(a,m),b.on(L.hide[c],q)),b.on("keypress",function(a){27===a.which&&q()})})}var D,E,F,G,H,I,J,K=angular.isDefined(n.appendToBody)?n.appendToBody:!1,L=p(void 0),M=angular.isDefined(d[k+"Enable"]),N=a.$new(!0),O=!1,P=angular.isDefined(d[k+"IsOpen"])?l(d[k+"IsOpen"]):!1,Q=n.useContentExp?l(d[e]):!1,R=[],S=function(){D&&D.html()&&(I||(I=g(function(){var a=i.positionElements(b,D,N.placement,K);D.css({top:a.top+"px",left:a.left+"px"}),D.hasClass(a.placement.split("-")[0])||(D.removeClass(J.split("-")[0]),D.addClass(a.placement.split("-")[0])),D.hasClass(n.placementClassPrefix+a.placement)||(D.removeClass(n.placementClassPrefix+J),D.addClass(n.placementClassPrefix+a.placement)),D.hasClass("uib-position-measure")?(i.positionArrow(D,a.placement),D.removeClass("uib-position-measure")):J!==a.placement&&i.positionArrow(D,a.placement),J=a.placement,I=null},0,!1)))};N.origScope=a,N.isOpen=!1,o.add(N,{close:t}),N.contentExp=function(){return N.content},d.$observe("disabled",function(a){a&&s(),a&&N.isOpen&&t()}),P&&a.$watch(P,function(a){N&&!a===N.isOpen&&j()});var T=function(){L.show.forEach(function(a){"outsideClick"===a?b.off("click",j):(b.off(a,m),b.off(a,j))}),L.hide.forEach(function(a){"outsideClick"===a?h.off("click",B):b.off(a,q)})};C();var U=a.$eval(d[k+"Animation"]);N.animation=angular.isDefined(U)?!!U:n.animation;var V,W=k+"AppendToBody";V=W in d&&void 0===d[W]?!0:a.$eval(d[W]),K=angular.isDefined(V)?V:K,a.$on("$destroy",function(){T(),w(),o.remove(N),N=null})}}}}}]}).directive("uibTooltipTemplateTransclude",["$animate","$sce","$compile","$templateRequest",function(a,b,c,d){return{link:function(e,f,g){var h,i,j,k=e.$eval(g.tooltipTemplateTranscludeScope),l=0,m=function(){i&&(i.remove(),i=null),h&&(h.$destroy(),h=null),j&&(a.leave(j).then(function(){i=null}),i=j,j=null)};e.$watch(b.parseAsResourceUrl(g.uibTooltipTemplateTransclude),function(b){var g=++l;b?(d(b,!0).then(function(d){if(g===l){var e=k.$new(),i=d,n=c(i)(e,function(b){m(),a.enter(b,f)});h=e,j=n,h.$emit("$includeContentLoaded",b)}},function(){g===l&&(m(),e.$emit("$includeContentError",b))}),e.$emit("$includeContentRequested",b)):m()}),e.$on("$destroy",m)}}}]).directive("uibTooltipClasses",["$uibPosition",function(a){return{restrict:"A",link:function(b,c,d){if(b.placement){var e=a.parsePlacement(b.placement);c.addClass(e[0])}b.popupClass&&c.addClass(b.popupClass),b.animation()&&c.addClass(d.tooltipAnimationClass)}}}]).directive("uibTooltipPopup",function(){return{replace:!0,scope:{content:"@",placement:"@",popupClass:"@",animation:"&",isOpen:"&"},templateUrl:"uib/template/tooltip/tooltip-popup.html"}}).directive("uibTooltip",["$uibTooltip",function(a){return a("uibTooltip","tooltip","mouseenter")}]).directive("uibTooltipTemplatePopup",function(){return{replace:!0,scope:{contentExp:"&",placement:"@",popupClass:"@",animation:"&",isOpen:"&",originScope:"&"},templateUrl:"uib/template/tooltip/tooltip-template-popup.html"}}).directive("uibTooltipTemplate",["$uibTooltip",function(a){return a("uibTooltipTemplate","tooltip","mouseenter",{useContentExp:!0})}]).directive("uibTooltipHtmlPopup",function(){return{replace:!0,scope:{contentExp:"&",placement:"@",popupClass:"@",animation:"&",isOpen:"&"},templateUrl:"uib/template/tooltip/tooltip-html-popup.html"}}).directive("uibTooltipHtml",["$uibTooltip",function(a){return a("uibTooltipHtml","tooltip","mouseenter",{useContentExp:!0})}]),angular.module("ui.bootstrap.popover",["ui.bootstrap.tooltip"]).directive("uibPopoverTemplatePopup",function(){return{replace:!0,scope:{uibTitle:"@",contentExp:"&",placement:"@",popupClass:"@",animation:"&",isOpen:"&",originScope:"&"},templateUrl:"uib/template/popover/popover-template.html"}}).directive("uibPopoverTemplate",["$uibTooltip",function(a){return a("uibPopoverTemplate","popover","click",{useContentExp:!0})}]).directive("uibPopoverHtmlPopup",function(){return{replace:!0,scope:{contentExp:"&",uibTitle:"@",placement:"@",popupClass:"@",animation:"&",isOpen:"&"},templateUrl:"uib/template/popover/popover-html.html"}}).directive("uibPopoverHtml",["$uibTooltip",function(a){return a("uibPopoverHtml","popover","click",{useContentExp:!0})}]).directive("uibPopoverPopup",function(){return{replace:!0,scope:{uibTitle:"@",content:"@",placement:"@",popupClass:"@",animation:"&",isOpen:"&"},templateUrl:"uib/template/popover/popover.html"}}).directive("uibPopover",["$uibTooltip",function(a){return a("uibPopover","popover","click")}]),angular.module("ui.bootstrap.progressbar",[]).constant("uibProgressConfig",{animate:!0,max:100}).controller("UibProgressController",["$scope","$attrs","uibProgressConfig",function(a,b,c){function d(){return angular.isDefined(a.maxParam)?a.maxParam:c.max}var e=this,f=angular.isDefined(b.animate)?a.$parent.$eval(b.animate):c.animate;this.bars=[],a.max=d(),this.addBar=function(a,b,c){f||b.css({transition:"none"}),this.bars.push(a),a.max=d(),a.title=c&&angular.isDefined(c.title)?c.title:"progressbar",a.$watch("value",function(b){a.recalculatePercentage()}),a.recalculatePercentage=function(){var b=e.bars.reduce(function(a,b){return b.percent=+(100*b.value/b.max).toFixed(2),a+b.percent},0);b>100&&(a.percent-=b-100)},a.$on("$destroy",function(){b=null,e.removeBar(a)})},this.removeBar=function(a){this.bars.splice(this.bars.indexOf(a),1),this.bars.forEach(function(a){a.recalculatePercentage()})},a.$watch("maxParam",function(a){e.bars.forEach(function(a){a.max=d(),a.recalculatePercentage()})})}]).directive("uibProgress",function(){return{replace:!0,transclude:!0,controller:"UibProgressController",require:"uibProgress",scope:{maxParam:"=?max"},templateUrl:"uib/template/progressbar/progress.html"}}).directive("uibBar",function(){return{replace:!0,transclude:!0,require:"^uibProgress",scope:{value:"=",type:"@"},templateUrl:"uib/template/progressbar/bar.html",link:function(a,b,c,d){d.addBar(a,b,c)}}}).directive("uibProgressbar",function(){return{replace:!0,transclude:!0,controller:"UibProgressController",scope:{value:"=",maxParam:"=?max",type:"@"},templateUrl:"uib/template/progressbar/progressbar.html",link:function(a,b,c,d){d.addBar(a,angular.element(b.children()[0]),{title:c.title})}}}),angular.module("ui.bootstrap.rating",[]).constant("uibRatingConfig",{max:5,stateOn:null,stateOff:null,enableReset:!0,titles:["one","two","three","four","five"]}).controller("UibRatingController",["$scope","$attrs","uibRatingConfig",function(a,b,c){var d={$setViewValue:angular.noop},e=this;this.init=function(e){d=e,d.$render=this.render,d.$formatters.push(function(a){return angular.isNumber(a)&&a<<0!==a&&(a=Math.round(a)),a}),this.stateOn=angular.isDefined(b.stateOn)?a.$parent.$eval(b.stateOn):c.stateOn,this.stateOff=angular.isDefined(b.stateOff)?a.$parent.$eval(b.stateOff):c.stateOff,this.enableReset=angular.isDefined(b.enableReset)?a.$parent.$eval(b.enableReset):c.enableReset;var f=angular.isDefined(b.titles)?a.$parent.$eval(b.titles):c.titles;this.titles=angular.isArray(f)&&f.length>0?f:c.titles;var g=angular.isDefined(b.ratingStates)?a.$parent.$eval(b.ratingStates):new Array(angular.isDefined(b.max)?a.$parent.$eval(b.max):c.max);a.range=this.buildTemplateObjects(g)},this.buildTemplateObjects=function(a){for(var b=0,c=a.length;c>b;b++)a[b]=angular.extend({index:b},{stateOn:this.stateOn,stateOff:this.stateOff,title:this.getTitle(b)},a[b]);return a},this.getTitle=function(a){return a>=this.titles.length?a+1:this.titles[a]},a.rate=function(b){if(!a.readonly&&b>=0&&b<=a.range.length){var c=e.enableReset&&d.$viewValue===b?0:b;d.$setViewValue(c),d.$render()}},a.enter=function(b){a.readonly||(a.value=b),a.onHover({value:b})},a.reset=function(){a.value=d.$viewValue,a.onLeave()},a.onKeydown=function(b){/(37|38|39|40)/.test(b.which)&&(b.preventDefault(),b.stopPropagation(),a.rate(a.value+(38===b.which||39===b.which?1:-1)))},this.render=function(){a.value=d.$viewValue,a.title=e.getTitle(a.value-1)}}]).directive("uibRating",function(){return{require:["uibRating","ngModel"],scope:{readonly:"=?readOnly",onHover:"&",onLeave:"&"},controller:"UibRatingController",templateUrl:"uib/template/rating/rating.html",replace:!0,link:function(a,b,c,d){var e=d[0],f=d[1];e.init(f)}}}),angular.module("ui.bootstrap.tabs",[]).controller("UibTabsetController",["$scope",function(a){function b(a){for(var b=0;b<d.tabs.length;b++)if(d.tabs[b].index===a)return b}var c,d=this;d.tabs=[],d.select=function(a,f){if(!e){var g=b(c),h=d.tabs[g];if(h){if(h.tab.onDeselect({$event:f,$selectedIndex:a}),f&&f.isDefaultPrevented())return;h.tab.active=!1}var i=d.tabs[a];i?(i.tab.onSelect({$event:f}),i.tab.active=!0,d.active=i.index,c=i.index):!i&&angular.isDefined(c)&&(d.active=null,c=null)}},d.addTab=function(a){if(d.tabs.push({tab:a,index:a.index}),d.tabs.sort(function(a,b){return a.index>b.index?1:a.index<b.index?-1:0}),a.index===d.active||!angular.isDefined(d.active)&&1===d.tabs.length){var c=b(a.index);d.select(c)}},d.removeTab=function(a){for(var b,c=0;c<d.tabs.length;c++)if(d.tabs[c].tab===a){b=c;break}if(d.tabs[b].index===d.active){var e=b===d.tabs.length-1?b-1:b+1%d.tabs.length;d.select(e)}d.tabs.splice(b,1)},a.$watch("tabset.active",function(a){angular.isDefined(a)&&a!==c&&d.select(b(a))});var e;a.$on("$destroy",function(){e=!0})}]).directive("uibTabset",function(){return{transclude:!0,replace:!0,scope:{},bindToController:{active:"=?",type:"@"},controller:"UibTabsetController",controllerAs:"tabset",templateUrl:function(a,b){return b.templateUrl||"uib/template/tabs/tabset.html"},link:function(a,b,c){a.vertical=angular.isDefined(c.vertical)?a.$parent.$eval(c.vertical):!1,a.justified=angular.isDefined(c.justified)?a.$parent.$eval(c.justified):!1}}}).directive("uibTab",["$parse",function(a){return{require:"^uibTabset",replace:!0,templateUrl:function(a,b){return b.templateUrl||"uib/template/tabs/tab.html"},transclude:!0,scope:{heading:"@",index:"=?",classes:"@?",onSelect:"&select",onDeselect:"&deselect"},controller:function(){},controllerAs:"tab",link:function(b,c,d,e,f){b.disabled=!1,d.disable&&b.$parent.$watch(a(d.disable),function(a){b.disabled=!!a}),angular.isUndefined(d.index)&&(e.tabs&&e.tabs.length?b.index=Math.max.apply(null,e.tabs.map(function(a){return a.index}))+1:b.index=0),angular.isUndefined(d.classes)&&(b.classes=""),b.select=function(a){if(!b.disabled){for(var c,d=0;d<e.tabs.length;d++)if(e.tabs[d].tab===b){c=d;break}e.select(c,a)}},e.addTab(b),b.$on("$destroy",function(){e.removeTab(b)}),b.$transcludeFn=f}}}]).directive("uibTabHeadingTransclude",function(){return{restrict:"A",require:"^uibTab",link:function(a,b){a.$watch("headingElement",function(a){a&&(b.html(""),b.append(a))})}}}).directive("uibTabContentTransclude",function(){function a(a){return a.tagName&&(a.hasAttribute("uib-tab-heading")||a.hasAttribute("data-uib-tab-heading")||a.hasAttribute("x-uib-tab-heading")||"uib-tab-heading"===a.tagName.toLowerCase()||"data-uib-tab-heading"===a.tagName.toLowerCase()||"x-uib-tab-heading"===a.tagName.toLowerCase()||"uib:tab-heading"===a.tagName.toLowerCase())}return{restrict:"A",require:"^uibTabset",link:function(b,c,d){var e=b.$eval(d.uibTabContentTransclude).tab;e.$transcludeFn(e.$parent,function(b){angular.forEach(b,function(b){a(b)?e.headingElement=b:c.append(b)})})}}}),angular.module("ui.bootstrap.timepicker",[]).constant("uibTimepickerConfig",{hourStep:1,minuteStep:1,secondStep:1,showMeridian:!0,showSeconds:!1,meridians:null,readonlyInput:!1,mousewheel:!0,arrowkeys:!0,showSpinners:!0,templateUrl:"uib/template/timepicker/timepicker.html"}).controller("UibTimepickerController",["$scope","$element","$attrs","$parse","$log","$locale","uibTimepickerConfig",function(a,b,c,d,e,f,g){function h(){var b=+a.hours,c=a.showMeridian?b>0&&13>b:b>=0&&24>b;return c&&""!==a.hours?(a.showMeridian&&(12===b&&(b=0),a.meridian===v[1]&&(b+=12)),b):void 0}function i(){var b=+a.minutes,c=b>=0&&60>b;return c&&""!==a.minutes?b:void 0}function j(){var b=+a.seconds;return b>=0&&60>b?b:void 0}function k(a,b){return null===a?"":angular.isDefined(a)&&a.toString().length<2&&!b?"0"+a:a.toString()}function l(a){m(),u.$setViewValue(new Date(s)),n(a)}function m(){u.$setValidity("time",!0),a.invalidHours=!1,a.invalidMinutes=!1,a.invalidSeconds=!1}function n(b){if(u.$modelValue){var c=s.getHours(),d=s.getMinutes(),e=s.getSeconds();a.showMeridian&&(c=0===c||12===c?12:c%12),a.hours="h"===b?c:k(c,!w),"m"!==b&&(a.minutes=k(d)),a.meridian=s.getHours()<12?v[0]:v[1],"s"!==b&&(a.seconds=k(e)),a.meridian=s.getHours()<12?v[0]:v[1]}else a.hours=null,a.minutes=null,a.seconds=null,a.meridian=v[0]}function o(a){s=q(s,a),l()}function p(a,b){return q(a,60*b)}function q(a,b){var c=new Date(a.getTime()+1e3*b),d=new Date(a);return d.setHours(c.getHours(),c.getMinutes(),c.getSeconds()),d}function r(){return(null===a.hours||""===a.hours)&&(null===a.minutes||""===a.minutes)&&(!a.showSeconds||a.showSeconds&&(null===a.seconds||""===a.seconds))}var s=new Date,t=[],u={$setViewValue:angular.noop},v=angular.isDefined(c.meridians)?a.$parent.$eval(c.meridians):g.meridians||f.DATETIME_FORMATS.AMPMS,w=angular.isDefined(c.padHours)?a.$parent.$eval(c.padHours):!0;a.tabindex=angular.isDefined(c.tabindex)?c.tabindex:0,b.removeAttr("tabindex"),this.init=function(b,d){u=b,u.$render=this.render,u.$formatters.unshift(function(a){return a?new Date(a):null});var e=d.eq(0),f=d.eq(1),h=d.eq(2),i=angular.isDefined(c.mousewheel)?a.$parent.$eval(c.mousewheel):g.mousewheel;i&&this.setupMousewheelEvents(e,f,h);var j=angular.isDefined(c.arrowkeys)?a.$parent.$eval(c.arrowkeys):g.arrowkeys;j&&this.setupArrowkeyEvents(e,f,h),a.readonlyInput=angular.isDefined(c.readonlyInput)?a.$parent.$eval(c.readonlyInput):g.readonlyInput,this.setupInputEvents(e,f,h)};var x=g.hourStep;c.hourStep&&t.push(a.$parent.$watch(d(c.hourStep),function(a){x=+a}));var y=g.minuteStep;c.minuteStep&&t.push(a.$parent.$watch(d(c.minuteStep),function(a){y=+a}));var z;t.push(a.$parent.$watch(d(c.min),function(a){var b=new Date(a);z=isNaN(b)?void 0:b}));var A;t.push(a.$parent.$watch(d(c.max),function(a){var b=new Date(a);A=isNaN(b)?void 0:b}));var B=!1;c.ngDisabled&&t.push(a.$parent.$watch(d(c.ngDisabled),function(a){B=a})),a.noIncrementHours=function(){var a=p(s,60*x);return B||a>A||s>a&&z>a},a.noDecrementHours=function(){var a=p(s,60*-x);return B||z>a||a>s&&a>A},a.noIncrementMinutes=function(){var a=p(s,y);return B||a>A||s>a&&z>a},a.noDecrementMinutes=function(){var a=p(s,-y);return B||z>a||a>s&&a>A},a.noIncrementSeconds=function(){var a=q(s,C);return B||a>A||s>a&&z>a},a.noDecrementSeconds=function(){var a=q(s,-C);return B||z>a||a>s&&a>A},a.noToggleMeridian=function(){return s.getHours()<12?B||p(s,720)>A:B||p(s,-720)<z};var C=g.secondStep;c.secondStep&&t.push(a.$parent.$watch(d(c.secondStep),function(a){C=+a})),a.showSeconds=g.showSeconds,c.showSeconds&&t.push(a.$parent.$watch(d(c.showSeconds),function(b){a.showSeconds=!!b})),a.showMeridian=g.showMeridian,c.showMeridian&&t.push(a.$parent.$watch(d(c.showMeridian),function(b){if(a.showMeridian=!!b,u.$error.time){var c=h(),d=i();angular.isDefined(c)&&angular.isDefined(d)&&(s.setHours(c),l())}else n()})),this.setupMousewheelEvents=function(b,c,d){var e=function(a){a.originalEvent&&(a=a.originalEvent);var b=a.wheelDelta?a.wheelDelta:-a.deltaY;return a.detail||b>0};b.bind("mousewheel wheel",function(b){B||a.$apply(e(b)?a.incrementHours():a.decrementHours()),b.preventDefault()}),c.bind("mousewheel wheel",function(b){B||a.$apply(e(b)?a.incrementMinutes():a.decrementMinutes()),b.preventDefault()}),d.bind("mousewheel wheel",function(b){B||a.$apply(e(b)?a.incrementSeconds():a.decrementSeconds()),b.preventDefault()})},this.setupArrowkeyEvents=function(b,c,d){b.bind("keydown",function(b){B||(38===b.which?(b.preventDefault(),a.incrementHours(),a.$apply()):40===b.which&&(b.preventDefault(),a.decrementHours(),a.$apply()))}),c.bind("keydown",function(b){B||(38===b.which?(b.preventDefault(),a.incrementMinutes(),a.$apply()):40===b.which&&(b.preventDefault(),a.decrementMinutes(),a.$apply()))}),d.bind("keydown",function(b){B||(38===b.which?(b.preventDefault(),a.incrementSeconds(),a.$apply()):40===b.which&&(b.preventDefault(),a.decrementSeconds(),a.$apply()))})},this.setupInputEvents=function(b,c,d){if(a.readonlyInput)return a.updateHours=angular.noop,a.updateMinutes=angular.noop,void(a.updateSeconds=angular.noop);var e=function(b,c,d){u.$setViewValue(null),u.$setValidity("time",!1),angular.isDefined(b)&&(a.invalidHours=b),angular.isDefined(c)&&(a.invalidMinutes=c),angular.isDefined(d)&&(a.invalidSeconds=d)};a.updateHours=function(){var a=h(),b=i();u.$setDirty(),angular.isDefined(a)&&angular.isDefined(b)?(s.setHours(a),s.setMinutes(b),z>s||s>A?e(!0):l("h")):e(!0)},b.bind("blur",function(b){u.$setTouched(),r()?m():null===a.hours||""===a.hours?e(!0):!a.invalidHours&&a.hours<10&&a.$apply(function(){a.hours=k(a.hours,!w)})}),a.updateMinutes=function(){var a=i(),b=h();u.$setDirty(),angular.isDefined(a)&&angular.isDefined(b)?(s.setHours(b),s.setMinutes(a),z>s||s>A?e(void 0,!0):l("m")):e(void 0,!0)},c.bind("blur",function(b){u.$setTouched(),r()?m():null===a.minutes?e(void 0,!0):!a.invalidMinutes&&a.minutes<10&&a.$apply(function(){a.minutes=k(a.minutes)})}),a.updateSeconds=function(){var a=j();u.$setDirty(),angular.isDefined(a)?(s.setSeconds(a),l("s")):e(void 0,void 0,!0)},d.bind("blur",function(b){r()?m():!a.invalidSeconds&&a.seconds<10&&a.$apply(function(){a.seconds=k(a.seconds)})})},this.render=function(){var b=u.$viewValue;isNaN(b)?(u.$setValidity("time",!1),e.error('Timepicker directive: "ng-model" value must be a Date object, a number of milliseconds since 01.01.1970 or a string representing an RFC2822 or ISO 8601 date.')):(b&&(s=b),z>s||s>A?(u.$setValidity("time",!1),a.invalidHours=!0,a.invalidMinutes=!0):m(),n())},a.showSpinners=angular.isDefined(c.showSpinners)?a.$parent.$eval(c.showSpinners):g.showSpinners,a.incrementHours=function(){a.noIncrementHours()||o(60*x*60)},a.decrementHours=function(){a.noDecrementHours()||o(60*-x*60)},a.incrementMinutes=function(){a.noIncrementMinutes()||o(60*y)},a.decrementMinutes=function(){a.noDecrementMinutes()||o(60*-y)},a.incrementSeconds=function(){a.noIncrementSeconds()||o(C)},a.decrementSeconds=function(){a.noDecrementSeconds()||o(-C)},a.toggleMeridian=function(){var b=i(),c=h();a.noToggleMeridian()||(angular.isDefined(b)&&angular.isDefined(c)?o(720*(s.getHours()<12?60:-60)):a.meridian=a.meridian===v[0]?v[1]:v[0])},a.blur=function(){u.$setTouched()},a.$on("$destroy",function(){for(;t.length;)t.shift()()})}]).directive("uibTimepicker",["uibTimepickerConfig",function(a){return{require:["uibTimepicker","?^ngModel"],controller:"UibTimepickerController",controllerAs:"timepicker",replace:!0,scope:{},templateUrl:function(b,c){return c.templateUrl||a.templateUrl},link:function(a,b,c,d){var e=d[0],f=d[1];f&&e.init(f,b.find("input"))}}}]),angular.module("ui.bootstrap.typeahead",["ui.bootstrap.debounce","ui.bootstrap.position"]).factory("uibTypeaheadParser",["$parse",function(a){var b=/^\s*([\s\S]+?)(?:\s+as\s+([\s\S]+?))?\s+for\s+(?:([\$\w][\$\w\d]*))\s+in\s+([\s\S]+?)$/;return{parse:function(c){var d=c.match(b);if(!d)throw new Error('Expected typeahead specification in form of "_modelValue_ (as _label_)? for _item_ in _collection_" but got "'+c+'".');return{itemName:d[3],source:a(d[4]),viewMapper:a(d[2]||d[1]),modelMapper:a(d[1])}}}}]).controller("UibTypeaheadController",["$scope","$element","$attrs","$compile","$parse","$q","$timeout","$document","$window","$rootScope","$$debounce","$uibPosition","uibTypeaheadParser",function(a,b,c,d,e,f,g,h,i,j,k,l,m){function n(){O.moveInProgress||(O.moveInProgress=!0,O.$digest()),Z()}function o(){O.position=E?l.offset(b):l.position(b),O.position.top+=b.prop("offsetHeight")}var p,q,r=[9,13,27,38,40],s=200,t=a.$eval(c.typeaheadMinLength);t||0===t||(t=1),a.$watch(c.typeaheadMinLength,function(a){t=a||0===a?a:1});var u=a.$eval(c.typeaheadWaitMs)||0,v=a.$eval(c.typeaheadEditable)!==!1;a.$watch(c.typeaheadEditable,function(a){v=a!==!1});var w,x,y=e(c.typeaheadLoading).assign||angular.noop,z=c.typeaheadShouldSelect?e(c.typeaheadShouldSelect):function(a,b){var c=b.$event;return 13===c.which||9===c.which},A=e(c.typeaheadOnSelect),B=angular.isDefined(c.typeaheadSelectOnBlur)?a.$eval(c.typeaheadSelectOnBlur):!1,C=e(c.typeaheadNoResults).assign||angular.noop,D=c.typeaheadInputFormatter?e(c.typeaheadInputFormatter):void 0,E=c.typeaheadAppendToBody?a.$eval(c.typeaheadAppendToBody):!1,F=c.typeaheadAppendTo?a.$eval(c.typeaheadAppendTo):null,G=a.$eval(c.typeaheadFocusFirst)!==!1,H=c.typeaheadSelectOnExact?a.$eval(c.typeaheadSelectOnExact):!1,I=e(c.typeaheadIsOpen).assign||angular.noop,J=a.$eval(c.typeaheadShowHint)||!1,K=e(c.ngModel),L=e(c.ngModel+"($$$p)"),M=function(b,c){return angular.isFunction(K(a))&&q&&q.$options&&q.$options.getterSetter?L(b,{$$$p:c}):K.assign(b,c)},N=m.parse(c.uibTypeahead),O=a.$new(),P=a.$on("$destroy",function(){O.$destroy()});O.$on("$destroy",P);var Q="typeahead-"+O.$id+"-"+Math.floor(1e4*Math.random());b.attr({"aria-autocomplete":"list","aria-expanded":!1,"aria-owns":Q});var R,S;J&&(R=angular.element("<div></div>"),R.css("position","relative"),b.after(R),S=b.clone(),S.attr("placeholder",""),S.attr("tabindex","-1"),S.val(""),S.css({position:"absolute",top:"0px",left:"0px","border-color":"transparent","box-shadow":"none",opacity:1,background:"none 0% 0% / auto repeat scroll padding-box border-box rgb(255, 255, 255)",color:"#999"}),b.css({position:"relative","vertical-align":"top","background-color":"transparent"}),R.append(S),S.after(b));var T=angular.element("<div uib-typeahead-popup></div>");T.attr({id:Q,matches:"matches",active:"activeIdx",select:"select(activeIdx, evt)","move-in-progress":"moveInProgress",query:"query",position:"position","assign-is-open":"assignIsOpen(isOpen)",debounce:"debounceUpdate"}),angular.isDefined(c.typeaheadTemplateUrl)&&T.attr("template-url",c.typeaheadTemplateUrl),angular.isDefined(c.typeaheadPopupTemplateUrl)&&T.attr("popup-template-url",c.typeaheadPopupTemplateUrl);var U=function(){J&&S.val("")},V=function(){O.matches=[],O.activeIdx=-1,b.attr("aria-expanded",!1),U()},W=function(a){return Q+"-option-"+a};O.$watch("activeIdx",function(a){0>a?b.removeAttr("aria-activedescendant"):b.attr("aria-activedescendant",W(a))});var X=function(a,b){return O.matches.length>b&&a?a.toUpperCase()===O.matches[b].label.toUpperCase():!1},Y=function(c,d){var e={$viewValue:c};y(a,!0),C(a,!1),f.when(N.source(a,e)).then(function(f){var g=c===p.$viewValue;if(g&&w)if(f&&f.length>0){O.activeIdx=G?0:-1,C(a,!1),O.matches.length=0;for(var h=0;h<f.length;h++)e[N.itemName]=f[h],O.matches.push({id:W(h),label:N.viewMapper(O,e),model:f[h]});if(O.query=c,o(),b.attr("aria-expanded",!0),H&&1===O.matches.length&&X(c,0)&&(angular.isNumber(O.debounceUpdate)||angular.isObject(O.debounceUpdate)?k(function(){O.select(0,d)},angular.isNumber(O.debounceUpdate)?O.debounceUpdate:O.debounceUpdate["default"]):O.select(0,d)),J){var i=O.matches[0].label;angular.isString(c)&&c.length>0&&i.slice(0,c.length).toUpperCase()===c.toUpperCase()?S.val(c+i.slice(c.length)):S.val("")}}else V(),C(a,!0);g&&y(a,!1)},function(){V(),y(a,!1),C(a,!0)})};E&&(angular.element(i).on("resize",n),h.find("body").on("scroll",n));var Z=k(function(){O.matches.length&&o(),O.moveInProgress=!1},s);O.moveInProgress=!1,O.query=void 0;var $,_=function(a){$=g(function(){Y(a)},u)},aa=function(){$&&g.cancel($)};V(),O.assignIsOpen=function(b){I(a,b)},O.select=function(d,e){var f,h,i={};x=!0,i[N.itemName]=h=O.matches[d].model,f=N.modelMapper(a,i),M(a,f),p.$setValidity("editable",!0),p.$setValidity("parse",!0),A(a,{$item:h,$model:f,$label:N.viewMapper(a,i),$event:e}),V(),O.$eval(c.typeaheadFocusOnSelect)!==!1&&g(function(){b[0].focus()},0,!1)},b.on("keydown",function(b){if(0!==O.matches.length&&-1!==r.indexOf(b.which)){var c=z(a,{$event:b});if(-1===O.activeIdx&&c||9===b.which&&b.shiftKey)return V(),void O.$digest();b.preventDefault();var d;switch(b.which){case 27:b.stopPropagation(),V(),a.$digest();break;case 38:O.activeIdx=(O.activeIdx>0?O.activeIdx:O.matches.length)-1,O.$digest(),d=T.find("li")[O.activeIdx],d.parentNode.scrollTop=d.offsetTop;break;case 40:O.activeIdx=(O.activeIdx+1)%O.matches.length,O.$digest(),d=T.find("li")[O.activeIdx],d.parentNode.scrollTop=d.offsetTop;break;default:c&&O.$apply(function(){angular.isNumber(O.debounceUpdate)||angular.isObject(O.debounceUpdate)?k(function(){O.select(O.activeIdx,b)},angular.isNumber(O.debounceUpdate)?O.debounceUpdate:O.debounceUpdate["default"]):O.select(O.activeIdx,b)})}}}),b.bind("focus",function(a){w=!0,0!==t||p.$viewValue||g(function(){Y(p.$viewValue,a)},0)}),b.bind("blur",function(a){B&&O.matches.length&&-1!==O.activeIdx&&!x&&(x=!0,O.$apply(function(){angular.isObject(O.debounceUpdate)&&angular.isNumber(O.debounceUpdate.blur)?k(function(){O.select(O.activeIdx,a)},O.debounceUpdate.blur):O.select(O.activeIdx,a)})),!v&&p.$error.editable&&(p.$setViewValue(),p.$setValidity("editable",!0),p.$setValidity("parse",!0),b.val("")),w=!1,x=!1});var ba=function(c){b[0]!==c.target&&3!==c.which&&0!==O.matches.length&&(V(),j.$$phase||a.$digest())};h.on("click",ba),a.$on("$destroy",function(){h.off("click",ba),(E||F)&&ca.remove(),E&&(angular.element(i).off("resize",n),h.find("body").off("scroll",n)),T.remove(),J&&R.remove()});var ca=d(T)(O);E?h.find("body").append(ca):F?angular.element(F).eq(0).append(ca):b.after(ca),this.init=function(b,c){p=b,q=c,O.debounceUpdate=p.$options&&e(p.$options.debounce)(a),p.$parsers.unshift(function(b){return w=!0,0===t||b&&b.length>=t?u>0?(aa(),_(b)):Y(b):(y(a,!1),aa(),V()),v?b:b?void p.$setValidity("editable",!1):(p.$setValidity("editable",!0),null)}),p.$formatters.push(function(b){var c,d,e={};return v||p.$setValidity("editable",!0),D?(e.$model=b,D(a,e)):(e[N.itemName]=b,c=N.viewMapper(a,e),e[N.itemName]=void 0,d=N.viewMapper(a,e),c!==d?c:b)})}}]).directive("uibTypeahead",function(){return{controller:"UibTypeaheadController",require:["ngModel","^?ngModelOptions","uibTypeahead"],link:function(a,b,c,d){d[2].init(d[0],d[1])}}}).directive("uibTypeaheadPopup",["$$debounce",function(a){return{scope:{matches:"=",query:"=",active:"=",position:"&",moveInProgress:"=",select:"&",assignIsOpen:"&",debounce:"&"},replace:!0,templateUrl:function(a,b){return b.popupTemplateUrl||"uib/template/typeahead/typeahead-popup.html"},link:function(b,c,d){b.templateUrl=d.templateUrl,b.isOpen=function(){var a=b.matches.length>0;return b.assignIsOpen({isOpen:a}),a},b.isActive=function(a){return b.active===a},b.selectActive=function(a){b.active=a},b.selectMatch=function(c,d){var e=b.debounce();angular.isNumber(e)||angular.isObject(e)?a(function(){b.select({activeIdx:c,evt:d})},angular.isNumber(e)?e:e["default"]):b.select({activeIdx:c,evt:d})}}}}]).directive("uibTypeaheadMatch",["$templateRequest","$compile","$parse",function(a,b,c){return{scope:{index:"=",match:"=",query:"="},link:function(d,e,f){var g=c(f.templateUrl)(d.$parent)||"uib/template/typeahead/typeahead-match.html";a(g).then(function(a){var c=angular.element(a.trim());e.replaceWith(c),b(c)(d)})}}}]).filter("uibTypeaheadHighlight",["$sce","$injector","$log",function(a,b,c){function d(a){return a.replace(/([.?*+^$[\]\\(){}|-])/g,"\\$1")}function e(a){return/<.*>/g.test(a)}var f;return f=b.has("$sanitize"),function(b,g){return!f&&e(b)&&c.warn("Unsafe use of typeahead please use ngSanitize"),b=g?(""+b).replace(new RegExp(d(g),"gi"),"<strong>$&</strong>"):b,f||(b=a.trustAsHtml(b)),b}}]),angular.module("uib/template/accordion/accordion-group.html",[]).run(["$templateCache",function(a){a.put("uib/template/accordion/accordion-group.html",'<div class="panel" ng-class="panelClass || \'panel-default\'">\n  <div role="tab" id="{{::headingId}}" aria-selected="{{isOpen}}" class="panel-heading" ng-keypress="toggleOpen($event)">\n    <h4 class="panel-title">\n      <a role="button" data-toggle="collapse" href aria-expanded="{{isOpen}}" aria-controls="{{::panelId}}" tabindex="0" class="accordion-toggle" ng-click="toggleOpen()" uib-accordion-transclude="heading"><span uib-accordion-header ng-class="{\'text-muted\': isDisabled}">{{heading}}</span></a>\n    </h4>\n  </div>\n  <div id="{{::panelId}}" aria-labelledby="{{::headingId}}" aria-hidden="{{!isOpen}}" role="tabpanel" class="panel-collapse collapse" uib-collapse="!isOpen">\n    <div class="panel-body" ng-transclude></div>\n  </div>\n</div>\n')}]),angular.module("uib/template/accordion/accordion.html",[]).run(["$templateCache",function(a){a.put("uib/template/accordion/accordion.html",'<div role="tablist" class="panel-group" ng-transclude></div>')}]),angular.module("uib/template/alert/alert.html",[]).run(["$templateCache",function(a){a.put("uib/template/alert/alert.html",'<div class="alert" ng-class="[\'alert-\' + (type || \'warning\'), closeable ? \'alert-dismissible\' : null]" role="alert">\n    <button ng-show="closeable" type="button" class="close" ng-click="close({$event: $event})">\n        <span aria-hidden="true">&times;</span>\n        <span class="sr-only">Close</span>\n    </button>\n    <div ng-transclude></div>\n</div>\n')}]),angular.module("uib/template/carousel/carousel.html",[]).run(["$templateCache",function(a){a.put("uib/template/carousel/carousel.html",'<div ng-mouseenter="pause()" ng-mouseleave="play()" class="carousel" ng-swipe-right="prev()" ng-swipe-left="next()">\n  <div class="carousel-inner" ng-transclude></div>\n  <a role="button" href class="left carousel-control" ng-click="prev()" ng-class="{ disabled: isPrevDisabled() }" ng-show="slides.length > 1">\n    <span aria-hidden="true" class="glyphicon glyphicon-chevron-left"></span>\n    <span class="sr-only">previous</span>\n  </a>\n  <a role="button" href class="right carousel-control" ng-click="next()" ng-class="{ disabled: isNextDisabled() }" ng-show="slides.length > 1">\n    <span aria-hidden="true" class="glyphicon glyphicon-chevron-right"></span>\n    <span class="sr-only">next</span>\n  </a>\n  <ol class="carousel-indicators" ng-show="slides.length > 1">\n    <li ng-repeat="slide in slides | orderBy:indexOfSlide track by $index" ng-class="{ active: isActive(slide) }" ng-click="select(slide)">\n      <span class="sr-only">slide {{ $index + 1 }} of {{ slides.length }}<span ng-if="isActive(slide)">, currently active</span></span>\n    </li>\n  </ol>\n</div>\n');
}]),angular.module("uib/template/carousel/slide.html",[]).run(["$templateCache",function(a){a.put("uib/template/carousel/slide.html",'<div ng-class="{\n    \'active\': active\n  }" class="item text-center" ng-transclude></div>\n')}]),angular.module("uib/template/datepicker/datepicker.html",[]).run(["$templateCache",function(a){a.put("uib/template/datepicker/datepicker.html",'<div class="uib-datepicker" ng-switch="datepickerMode" role="application" ng-keydown="keydown($event)">\n  <uib-daypicker ng-switch-when="day" tabindex="0"></uib-daypicker>\n  <uib-monthpicker ng-switch-when="month" tabindex="0"></uib-monthpicker>\n  <uib-yearpicker ng-switch-when="year" tabindex="0"></uib-yearpicker>\n</div>\n')}]),angular.module("uib/template/datepicker/day.html",[]).run(["$templateCache",function(a){a.put("uib/template/datepicker/day.html",'<table class="uib-daypicker" role="grid" aria-labelledby="{{::uniqueId}}-title" aria-activedescendant="{{activeDateId}}">\n  <thead>\n    <tr>\n      <th><button type="button" class="btn btn-default btn-sm pull-left uib-left" ng-click="move(-1)" tabindex="-1"><i class="glyphicon glyphicon-chevron-left"></i></button></th>\n      <th colspan="{{::5 + showWeeks}}"><button id="{{::uniqueId}}-title" role="heading" aria-live="assertive" aria-atomic="true" type="button" class="btn btn-default btn-sm uib-title" ng-click="toggleMode()" ng-disabled="datepickerMode === maxMode" tabindex="-1"><strong>{{title}}</strong></button></th>\n      <th><button type="button" class="btn btn-default btn-sm pull-right uib-right" ng-click="move(1)" tabindex="-1"><i class="glyphicon glyphicon-chevron-right"></i></button></th>\n    </tr>\n    <tr>\n      <th ng-if="showWeeks" class="text-center"></th>\n      <th ng-repeat="label in ::labels track by $index" class="text-center"><small aria-label="{{::label.full}}">{{::label.abbr}}</small></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr class="uib-weeks" ng-repeat="row in rows track by $index">\n      <td ng-if="showWeeks" class="text-center h6"><em>{{ weekNumbers[$index] }}</em></td>\n      <td ng-repeat="dt in row" class="uib-day text-center" role="gridcell"\n        id="{{::dt.uid}}"\n        ng-class="::dt.customClass">\n        <button type="button" class="btn btn-default btn-sm"\n          uib-is-class="\n            \'btn-info\' for selectedDt,\n            \'active\' for activeDt\n            on dt"\n          ng-click="select(dt.date)"\n          ng-disabled="::dt.disabled"\n          tabindex="-1"><span ng-class="::{\'text-muted\': dt.secondary, \'text-info\': dt.current}">{{::dt.label}}</span></button>\n      </td>\n    </tr>\n  </tbody>\n</table>\n')}]),angular.module("uib/template/datepicker/month.html",[]).run(["$templateCache",function(a){a.put("uib/template/datepicker/month.html",'<table class="uib-monthpicker" role="grid" aria-labelledby="{{::uniqueId}}-title" aria-activedescendant="{{activeDateId}}">\n  <thead>\n    <tr>\n      <th><button type="button" class="btn btn-default btn-sm pull-left uib-left" ng-click="move(-1)" tabindex="-1"><i class="glyphicon glyphicon-chevron-left"></i></button></th>\n      <th><button id="{{::uniqueId}}-title" role="heading" aria-live="assertive" aria-atomic="true" type="button" class="btn btn-default btn-sm uib-title" ng-click="toggleMode()" ng-disabled="datepickerMode === maxMode" tabindex="-1"><strong>{{title}}</strong></button></th>\n      <th><button type="button" class="btn btn-default btn-sm pull-right uib-right" ng-click="move(1)" tabindex="-1"><i class="glyphicon glyphicon-chevron-right"></i></button></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr class="uib-months" ng-repeat="row in rows track by $index">\n      <td ng-repeat="dt in row" class="uib-month text-center" role="gridcell"\n        id="{{::dt.uid}}"\n        ng-class="::dt.customClass">\n        <button type="button" class="btn btn-default"\n          uib-is-class="\n            \'btn-info\' for selectedDt,\n            \'active\' for activeDt\n            on dt"\n          ng-click="select(dt.date)"\n          ng-disabled="::dt.disabled"\n          tabindex="-1"><span ng-class="::{\'text-info\': dt.current}">{{::dt.label}}</span></button>\n      </td>\n    </tr>\n  </tbody>\n</table>\n')}]),angular.module("uib/template/datepicker/year.html",[]).run(["$templateCache",function(a){a.put("uib/template/datepicker/year.html",'<table class="uib-yearpicker" role="grid" aria-labelledby="{{::uniqueId}}-title" aria-activedescendant="{{activeDateId}}">\n  <thead>\n    <tr>\n      <th><button type="button" class="btn btn-default btn-sm pull-left uib-left" ng-click="move(-1)" tabindex="-1"><i class="glyphicon glyphicon-chevron-left"></i></button></th>\n      <th colspan="{{::columns - 2}}"><button id="{{::uniqueId}}-title" role="heading" aria-live="assertive" aria-atomic="true" type="button" class="btn btn-default btn-sm uib-title" ng-click="toggleMode()" ng-disabled="datepickerMode === maxMode" tabindex="-1"><strong>{{title}}</strong></button></th>\n      <th><button type="button" class="btn btn-default btn-sm pull-right uib-right" ng-click="move(1)" tabindex="-1"><i class="glyphicon glyphicon-chevron-right"></i></button></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr class="uib-years" ng-repeat="row in rows track by $index">\n      <td ng-repeat="dt in row" class="uib-year text-center" role="gridcell"\n        id="{{::dt.uid}}"\n        ng-class="::dt.customClass">\n        <button type="button" class="btn btn-default"\n          uib-is-class="\n            \'btn-info\' for selectedDt,\n            \'active\' for activeDt\n            on dt"\n          ng-click="select(dt.date)"\n          ng-disabled="::dt.disabled"\n          tabindex="-1"><span ng-class="::{\'text-info\': dt.current}">{{::dt.label}}</span></button>\n      </td>\n    </tr>\n  </tbody>\n</table>\n')}]),angular.module("uib/template/datepickerPopup/popup.html",[]).run(["$templateCache",function(a){a.put("uib/template/datepickerPopup/popup.html",'<div>\n  <ul class="uib-datepicker-popup dropdown-menu uib-position-measure" dropdown-nested ng-if="isOpen" ng-keydown="keydown($event)" ng-click="$event.stopPropagation()">\n    <li ng-transclude></li>\n    <li ng-if="showButtonBar" class="uib-button-bar">\n      <span class="btn-group pull-left">\n        <button type="button" class="btn btn-sm btn-info uib-datepicker-current" ng-click="select(\'today\', $event)" ng-disabled="isDisabled(\'today\')">{{ getText(\'current\') }}</button>\n        <button type="button" class="btn btn-sm btn-danger uib-clear" ng-click="select(null, $event)">{{ getText(\'clear\') }}</button>\n      </span>\n      <button type="button" class="btn btn-sm btn-success pull-right uib-close" ng-click="close($event)">{{ getText(\'close\') }}</button>\n    </li>\n  </ul>\n</div>\n')}]),angular.module("uib/template/modal/backdrop.html",[]).run(["$templateCache",function(a){a.put("uib/template/modal/backdrop.html",'<div class="modal-backdrop"\n     uib-modal-animation-class="fade"\n     modal-in-class="in"\n     ng-style="{\'z-index\': 1040 + (index && 1 || 0) + index*10}"\n></div>\n')}]),angular.module("uib/template/modal/window.html",[]).run(["$templateCache",function(a){a.put("uib/template/modal/window.html",'<div modal-render="{{$isRendered}}" tabindex="-1" role="dialog" class="modal"\n    uib-modal-animation-class="fade"\n    modal-in-class="in"\n    ng-style="{\'z-index\': 1050 + index*10, display: \'block\'}">\n    <div class="modal-dialog {{size ? \'modal-\' + size : \'\'}}"><div class="modal-content" uib-modal-transclude></div></div>\n</div>\n')}]),angular.module("uib/template/pager/pager.html",[]).run(["$templateCache",function(a){a.put("uib/template/pager/pager.html",'<ul class="pager">\n  <li ng-class="{disabled: noPrevious()||ngDisabled, previous: align}"><a href ng-click="selectPage(page - 1, $event)">{{::getText(\'previous\')}}</a></li>\n  <li ng-class="{disabled: noNext()||ngDisabled, next: align}"><a href ng-click="selectPage(page + 1, $event)">{{::getText(\'next\')}}</a></li>\n</ul>\n')}]),angular.module("uib/template/pagination/pagination.html",[]).run(["$templateCache",function(a){a.put("uib/template/pagination/pagination.html",'<ul class="pagination">\n  <li ng-if="::boundaryLinks" ng-class="{disabled: noPrevious()||ngDisabled}" class="pagination-first"><a href ng-click="selectPage(1, $event)">{{::getText(\'first\')}}</a></li>\n  <li ng-if="::directionLinks" ng-class="{disabled: noPrevious()||ngDisabled}" class="pagination-prev"><a href ng-click="selectPage(page - 1, $event)">{{::getText(\'previous\')}}</a></li>\n  <li ng-repeat="page in pages track by $index" ng-class="{active: page.active,disabled: ngDisabled&&!page.active}" class="pagination-page"><a href ng-click="selectPage(page.number, $event)">{{page.text}}</a></li>\n  <li ng-if="::directionLinks" ng-class="{disabled: noNext()||ngDisabled}" class="pagination-next"><a href ng-click="selectPage(page + 1, $event)">{{::getText(\'next\')}}</a></li>\n  <li ng-if="::boundaryLinks" ng-class="{disabled: noNext()||ngDisabled}" class="pagination-last"><a href ng-click="selectPage(totalPages, $event)">{{::getText(\'last\')}}</a></li>\n</ul>\n')}]),angular.module("uib/template/tooltip/tooltip-html-popup.html",[]).run(["$templateCache",function(a){a.put("uib/template/tooltip/tooltip-html-popup.html",'<div class="tooltip"\n  tooltip-animation-class="fade"\n  uib-tooltip-classes\n  ng-class="{ in: isOpen() }">\n  <div class="tooltip-arrow"></div>\n  <div class="tooltip-inner" ng-bind-html="contentExp()"></div>\n</div>\n')}]),angular.module("uib/template/tooltip/tooltip-popup.html",[]).run(["$templateCache",function(a){a.put("uib/template/tooltip/tooltip-popup.html",'<div class="tooltip"\n  tooltip-animation-class="fade"\n  uib-tooltip-classes\n  ng-class="{ in: isOpen() }">\n  <div class="tooltip-arrow"></div>\n  <div class="tooltip-inner" ng-bind="content"></div>\n</div>\n')}]),angular.module("uib/template/tooltip/tooltip-template-popup.html",[]).run(["$templateCache",function(a){a.put("uib/template/tooltip/tooltip-template-popup.html",'<div class="tooltip"\n  tooltip-animation-class="fade"\n  uib-tooltip-classes\n  ng-class="{ in: isOpen() }">\n  <div class="tooltip-arrow"></div>\n  <div class="tooltip-inner"\n    uib-tooltip-template-transclude="contentExp()"\n    tooltip-template-transclude-scope="originScope()"></div>\n</div>\n')}]),angular.module("uib/template/popover/popover-html.html",[]).run(["$templateCache",function(a){a.put("uib/template/popover/popover-html.html",'<div class="popover"\n  tooltip-animation-class="fade"\n  uib-tooltip-classes\n  ng-class="{ in: isOpen() }">\n  <div class="arrow"></div>\n\n  <div class="popover-inner">\n      <h3 class="popover-title" ng-bind="uibTitle" ng-if="uibTitle"></h3>\n      <div class="popover-content" ng-bind-html="contentExp()"></div>\n  </div>\n</div>\n')}]),angular.module("uib/template/popover/popover-template.html",[]).run(["$templateCache",function(a){a.put("uib/template/popover/popover-template.html",'<div class="popover"\n  tooltip-animation-class="fade"\n  uib-tooltip-classes\n  ng-class="{ in: isOpen() }">\n  <div class="arrow"></div>\n\n  <div class="popover-inner">\n      <h3 class="popover-title" ng-bind="uibTitle" ng-if="uibTitle"></h3>\n      <div class="popover-content"\n        uib-tooltip-template-transclude="contentExp()"\n        tooltip-template-transclude-scope="originScope()"></div>\n  </div>\n</div>\n')}]),angular.module("uib/template/popover/popover.html",[]).run(["$templateCache",function(a){a.put("uib/template/popover/popover.html",'<div class="popover"\n  tooltip-animation-class="fade"\n  uib-tooltip-classes\n  ng-class="{ in: isOpen() }">\n  <div class="arrow"></div>\n\n  <div class="popover-inner">\n      <h3 class="popover-title" ng-bind="uibTitle" ng-if="uibTitle"></h3>\n      <div class="popover-content" ng-bind="content"></div>\n  </div>\n</div>\n')}]),angular.module("uib/template/progressbar/bar.html",[]).run(["$templateCache",function(a){a.put("uib/template/progressbar/bar.html",'<div class="progress-bar" ng-class="type && \'progress-bar-\' + type" role="progressbar" aria-valuenow="{{value}}" aria-valuemin="0" aria-valuemax="{{max}}" ng-style="{width: (percent < 100 ? percent : 100) + \'%\'}" aria-valuetext="{{percent | number:0}}%" aria-labelledby="{{::title}}" ng-transclude></div>\n')}]),angular.module("uib/template/progressbar/progress.html",[]).run(["$templateCache",function(a){a.put("uib/template/progressbar/progress.html",'<div class="progress" ng-transclude aria-labelledby="{{::title}}"></div>')}]),angular.module("uib/template/progressbar/progressbar.html",[]).run(["$templateCache",function(a){a.put("uib/template/progressbar/progressbar.html",'<div class="progress">\n  <div class="progress-bar" ng-class="type && \'progress-bar-\' + type" role="progressbar" aria-valuenow="{{value}}" aria-valuemin="0" aria-valuemax="{{max}}" ng-style="{width: (percent < 100 ? percent : 100) + \'%\'}" aria-valuetext="{{percent | number:0}}%" aria-labelledby="{{::title}}" ng-transclude></div>\n</div>\n')}]),angular.module("uib/template/rating/rating.html",[]).run(["$templateCache",function(a){a.put("uib/template/rating/rating.html",'<span ng-mouseleave="reset()" ng-keydown="onKeydown($event)" tabindex="0" role="slider" aria-valuemin="0" aria-valuemax="{{range.length}}" aria-valuenow="{{value}}" aria-valuetext="{{title}}">\n    <span ng-repeat-start="r in range track by $index" class="sr-only">({{ $index < value ? \'*\' : \' \' }})</span>\n    <i ng-repeat-end ng-mouseenter="enter($index + 1)" ng-click="rate($index + 1)" class="glyphicon" ng-class="$index < value && (r.stateOn || \'glyphicon-star\') || (r.stateOff || \'glyphicon-star-empty\')" ng-attr-title="{{r.title}}"></i>\n</span>\n')}]),angular.module("uib/template/tabs/tab.html",[]).run(["$templateCache",function(a){a.put("uib/template/tabs/tab.html",'<li ng-class="[{active: active, disabled: disabled}, classes]" class="uib-tab nav-item">\n  <a href ng-click="select($event)" class="nav-link" uib-tab-heading-transclude>{{heading}}</a>\n</li>\n')}]),angular.module("uib/template/tabs/tabset.html",[]).run(["$templateCache",function(a){a.put("uib/template/tabs/tabset.html",'<div>\n  <ul class="nav nav-{{tabset.type || \'tabs\'}}" ng-class="{\'nav-stacked\': vertical, \'nav-justified\': justified}" ng-transclude></ul>\n  <div class="tab-content">\n    <div class="tab-pane"\n         ng-repeat="tab in tabset.tabs"\n         ng-class="{active: tabset.active === tab.index}"\n         uib-tab-content-transclude="tab">\n    </div>\n  </div>\n</div>\n')}]),angular.module("uib/template/timepicker/timepicker.html",[]).run(["$templateCache",function(a){a.put("uib/template/timepicker/timepicker.html",'<table class="uib-timepicker">\n  <tbody>\n    <tr class="text-center" ng-show="::showSpinners">\n      <td class="uib-increment hours"><a ng-click="incrementHours()" ng-class="{disabled: noIncrementHours()}" class="btn btn-link" ng-disabled="noIncrementHours()" tabindex="{{::tabindex}}"><span class="glyphicon glyphicon-chevron-up"></span></a></td>\n      <td>&nbsp;</td>\n      <td class="uib-increment minutes"><a ng-click="incrementMinutes()" ng-class="{disabled: noIncrementMinutes()}" class="btn btn-link" ng-disabled="noIncrementMinutes()" tabindex="{{::tabindex}}"><span class="glyphicon glyphicon-chevron-up"></span></a></td>\n      <td ng-show="showSeconds">&nbsp;</td>\n      <td ng-show="showSeconds" class="uib-increment seconds"><a ng-click="incrementSeconds()" ng-class="{disabled: noIncrementSeconds()}" class="btn btn-link" ng-disabled="noIncrementSeconds()" tabindex="{{::tabindex}}"><span class="glyphicon glyphicon-chevron-up"></span></a></td>\n      <td ng-show="showMeridian"></td>\n    </tr>\n    <tr>\n      <td class="form-group uib-time hours" ng-class="{\'has-error\': invalidHours}">\n        <input type="text" placeholder="HH" ng-model="hours" ng-change="updateHours()" class="form-control text-center" ng-readonly="::readonlyInput" maxlength="2" tabindex="{{::tabindex}}" ng-disabled="noIncrementHours()" ng-blur="blur()">\n      </td>\n      <td class="uib-separator">:</td>\n      <td class="form-group uib-time minutes" ng-class="{\'has-error\': invalidMinutes}">\n        <input type="text" placeholder="MM" ng-model="minutes" ng-change="updateMinutes()" class="form-control text-center" ng-readonly="::readonlyInput" maxlength="2" tabindex="{{::tabindex}}" ng-disabled="noIncrementMinutes()" ng-blur="blur()">\n      </td>\n      <td ng-show="showSeconds" class="uib-separator">:</td>\n      <td class="form-group uib-time seconds" ng-class="{\'has-error\': invalidSeconds}" ng-show="showSeconds">\n        <input type="text" placeholder="SS" ng-model="seconds" ng-change="updateSeconds()" class="form-control text-center" ng-readonly="readonlyInput" maxlength="2" tabindex="{{::tabindex}}" ng-disabled="noIncrementSeconds()" ng-blur="blur()">\n      </td>\n      <td ng-show="showMeridian" class="uib-time am-pm"><button type="button" ng-class="{disabled: noToggleMeridian()}" class="btn btn-default text-center" ng-click="toggleMeridian()" ng-disabled="noToggleMeridian()" tabindex="{{::tabindex}}">{{meridian}}</button></td>\n    </tr>\n    <tr class="text-center" ng-show="::showSpinners">\n      <td class="uib-decrement hours"><a ng-click="decrementHours()" ng-class="{disabled: noDecrementHours()}" class="btn btn-link" ng-disabled="noDecrementHours()" tabindex="{{::tabindex}}"><span class="glyphicon glyphicon-chevron-down"></span></a></td>\n      <td>&nbsp;</td>\n      <td class="uib-decrement minutes"><a ng-click="decrementMinutes()" ng-class="{disabled: noDecrementMinutes()}" class="btn btn-link" ng-disabled="noDecrementMinutes()" tabindex="{{::tabindex}}"><span class="glyphicon glyphicon-chevron-down"></span></a></td>\n      <td ng-show="showSeconds">&nbsp;</td>\n      <td ng-show="showSeconds" class="uib-decrement seconds"><a ng-click="decrementSeconds()" ng-class="{disabled: noDecrementSeconds()}" class="btn btn-link" ng-disabled="noDecrementSeconds()" tabindex="{{::tabindex}}"><span class="glyphicon glyphicon-chevron-down"></span></a></td>\n      <td ng-show="showMeridian"></td>\n    </tr>\n  </tbody>\n</table>\n')}]),angular.module("uib/template/typeahead/typeahead-match.html",[]).run(["$templateCache",function(a){a.put("uib/template/typeahead/typeahead-match.html",'<a href\n   tabindex="-1"\n   ng-bind-html="match.label | uibTypeaheadHighlight:query"\n   ng-attr-title="{{match.label}}"></a>\n')}]),angular.module("uib/template/typeahead/typeahead-popup.html",[]).run(["$templateCache",function(a){a.put("uib/template/typeahead/typeahead-popup.html",'<ul class="dropdown-menu" ng-show="isOpen() && !moveInProgress" ng-style="{top: position().top+\'px\', left: position().left+\'px\'}" role="listbox" aria-hidden="{{!isOpen()}}">\n    <li ng-repeat="match in matches track by $index" ng-class="{active: isActive($index) }" ng-mouseenter="selectActive($index)" ng-click="selectMatch($index, $event)" role="option" id="{{::match.id}}">\n        <div uib-typeahead-match index="$index" match="match" query="query" template-url="templateUrl"></div>\n    </li>\n</ul>\n')}]),angular.module("ui.bootstrap.carousel").run(function(){!angular.$$csp().noInlineStyle&&!angular.$$uibCarouselCss&&angular.element(document).find("head").prepend('<style type="text/css">.ng-animate.item:not(.left):not(.right){-webkit-transition:0s ease-in-out left;transition:0s ease-in-out left}</style>'),angular.$$uibCarouselCss=!0}),angular.module("ui.bootstrap.datepicker").run(function(){!angular.$$csp().noInlineStyle&&!angular.$$uibDatepickerCss&&angular.element(document).find("head").prepend('<style type="text/css">.uib-datepicker .uib-title{width:100%;}.uib-day button,.uib-month button,.uib-year button{min-width:100%;}.uib-left,.uib-right{width:100%}</style>'),angular.$$uibDatepickerCss=!0}),angular.module("ui.bootstrap.position").run(function(){!angular.$$csp().noInlineStyle&&!angular.$$uibPositionCss&&angular.element(document).find("head").prepend('<style type="text/css">.uib-position-measure{display:block !important;visibility:hidden !important;position:absolute !important;top:-9999px !important;left:-9999px !important;}.uib-position-scrollbar-measure{position:absolute !important;top:-9999px !important;width:50px !important;height:50px !important;overflow:scroll !important;}.uib-position-body-scrollbar-measure{overflow:scroll !important;}</style>'),angular.$$uibPositionCss=!0}),angular.module("ui.bootstrap.datepickerPopup").run(function(){!angular.$$csp().noInlineStyle&&!angular.$$uibDatepickerpopupCss&&angular.element(document).find("head").prepend('<style type="text/css">.uib-datepicker-popup.dropdown-menu{display:block;float:none;margin:0;}.uib-button-bar{padding:10px 9px 2px;}</style>'),angular.$$uibDatepickerpopupCss=!0}),angular.module("ui.bootstrap.tooltip").run(function(){!angular.$$csp().noInlineStyle&&!angular.$$uibTooltipCss&&angular.element(document).find("head").prepend('<style type="text/css">[uib-tooltip-popup].tooltip.top-left > .tooltip-arrow,[uib-tooltip-popup].tooltip.top-right > .tooltip-arrow,[uib-tooltip-popup].tooltip.bottom-left > .tooltip-arrow,[uib-tooltip-popup].tooltip.bottom-right > .tooltip-arrow,[uib-tooltip-popup].tooltip.left-top > .tooltip-arrow,[uib-tooltip-popup].tooltip.left-bottom > .tooltip-arrow,[uib-tooltip-popup].tooltip.right-top > .tooltip-arrow,[uib-tooltip-popup].tooltip.right-bottom > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.top-left > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.top-right > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.bottom-left > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.bottom-right > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.left-top > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.left-bottom > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.right-top > .tooltip-arrow,[uib-tooltip-html-popup].tooltip.right-bottom > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.top-left > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.top-right > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.bottom-left > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.bottom-right > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.left-top > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.left-bottom > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.right-top > .tooltip-arrow,[uib-tooltip-template-popup].tooltip.right-bottom > .tooltip-arrow,[uib-popover-popup].popover.top-left > .arrow,[uib-popover-popup].popover.top-right > .arrow,[uib-popover-popup].popover.bottom-left > .arrow,[uib-popover-popup].popover.bottom-right > .arrow,[uib-popover-popup].popover.left-top > .arrow,[uib-popover-popup].popover.left-bottom > .arrow,[uib-popover-popup].popover.right-top > .arrow,[uib-popover-popup].popover.right-bottom > .arrow,[uib-popover-html-popup].popover.top-left > .arrow,[uib-popover-html-popup].popover.top-right > .arrow,[uib-popover-html-popup].popover.bottom-left > .arrow,[uib-popover-html-popup].popover.bottom-right > .arrow,[uib-popover-html-popup].popover.left-top > .arrow,[uib-popover-html-popup].popover.left-bottom > .arrow,[uib-popover-html-popup].popover.right-top > .arrow,[uib-popover-html-popup].popover.right-bottom > .arrow,[uib-popover-template-popup].popover.top-left > .arrow,[uib-popover-template-popup].popover.top-right > .arrow,[uib-popover-template-popup].popover.bottom-left > .arrow,[uib-popover-template-popup].popover.bottom-right > .arrow,[uib-popover-template-popup].popover.left-top > .arrow,[uib-popover-template-popup].popover.left-bottom > .arrow,[uib-popover-template-popup].popover.right-top > .arrow,[uib-popover-template-popup].popover.right-bottom > .arrow{top:auto;bottom:auto;left:auto;right:auto;margin:0;}[uib-popover-popup].popover,[uib-popover-html-popup].popover,[uib-popover-template-popup].popover{display:block !important;}</style>'),angular.$$uibTooltipCss=!0}),angular.module("ui.bootstrap.timepicker").run(function(){!angular.$$csp().noInlineStyle&&!angular.$$uibTimepickerCss&&angular.element(document).find("head").prepend('<style type="text/css">.uib-time input{width:50px;}</style>'),angular.$$uibTimepickerCss=!0}),angular.module("ui.bootstrap.typeahead").run(function(){!angular.$$csp().noInlineStyle&&!angular.$$uibTypeaheadCss&&angular.element(document).find("head").prepend('<style type="text/css">[uib-typeahead-popup].dropdown-menu{display:block;}</style>'),angular.$$uibTypeaheadCss=!0});;/**
 * @license AngularJS v1.5.8
 * (c) 2010-2016 Google, Inc. http://angularjs.org
 * License: MIT
 */
(function(window, angular) {'use strict';

var $resourceMinErr = angular.$$minErr('$resource');

// Helper functions and regex to lookup a dotted path on an object
// stopping at undefined/null.  The path must be composed of ASCII
// identifiers (just like $parse)
var MEMBER_NAME_REGEX = /^(\.[a-zA-Z_$@][0-9a-zA-Z_$@]*)+$/;

function isValidDottedPath(path) {
  return (path != null && path !== '' && path !== 'hasOwnProperty' &&
      MEMBER_NAME_REGEX.test('.' + path));
}

function lookupDottedPath(obj, path) {
  if (!isValidDottedPath(path)) {
    throw $resourceMinErr('badmember', 'Dotted member path "@{0}" is invalid.', path);
  }
  var keys = path.split('.');
  for (var i = 0, ii = keys.length; i < ii && angular.isDefined(obj); i++) {
    var key = keys[i];
    obj = (obj !== null) ? obj[key] : undefined;
  }
  return obj;
}

/**
 * Create a shallow copy of an object and clear other fields from the destination
 */
function shallowClearAndCopy(src, dst) {
  dst = dst || {};

  angular.forEach(dst, function(value, key) {
    delete dst[key];
  });

  for (var key in src) {
    if (src.hasOwnProperty(key) && !(key.charAt(0) === '$' && key.charAt(1) === '$')) {
      dst[key] = src[key];
    }
  }

  return dst;
}

/**
 * @ngdoc module
 * @name ngResource
 * @description
 *
 * # ngResource
 *
 * The `ngResource` module provides interaction support with RESTful services
 * via the $resource service.
 *
 *
 * <div doc-module-components="ngResource"></div>
 *
 * See {@link ngResource.$resourceProvider} and {@link ngResource.$resource} for usage.
 */

/**
 * @ngdoc provider
 * @name $resourceProvider
 *
 * @description
 *
 * Use `$resourceProvider` to change the default behavior of the {@link ngResource.$resource}
 * service.
 *
 * ## Dependencies
 * Requires the {@link ngResource } module to be installed.
 *
 */

/**
 * @ngdoc service
 * @name $resource
 * @requires $http
 * @requires ng.$log
 * @requires $q
 * @requires ng.$timeout
 *
 * @description
 * A factory which creates a resource object that lets you interact with
 * [RESTful](http://en.wikipedia.org/wiki/Representational_State_Transfer) server-side data sources.
 *
 * The returned resource object has action methods which provide high-level behaviors without
 * the need to interact with the low level {@link ng.$http $http} service.
 *
 * Requires the {@link ngResource `ngResource`} module to be installed.
 *
 * By default, trailing slashes will be stripped from the calculated URLs,
 * which can pose problems with server backends that do not expect that
 * behavior.  This can be disabled by configuring the `$resourceProvider` like
 * this:
 *
 * ```js
     app.config(['$resourceProvider', function($resourceProvider) {
       // Don't strip trailing slashes from calculated URLs
       $resourceProvider.defaults.stripTrailingSlashes = false;
     }]);
 * ```
 *
 * @param {string} url A parameterized URL template with parameters prefixed by `:` as in
 *   `/user/:username`. If you are using a URL with a port number (e.g.
 *   `http://example.com:8080/api`), it will be respected.
 *
 *   If you are using a url with a suffix, just add the suffix, like this:
 *   `$resource('http://example.com/resource.json')` or `$resource('http://example.com/:id.json')`
 *   or even `$resource('http://example.com/resource/:resource_id.:format')`
 *   If the parameter before the suffix is empty, :resource_id in this case, then the `/.` will be
 *   collapsed down to a single `.`.  If you need this sequence to appear and not collapse then you
 *   can escape it with `/\.`.
 *
 * @param {Object=} paramDefaults Default values for `url` parameters. These can be overridden in
 *   `actions` methods. If a parameter value is a function, it will be called every time
 *   a param value needs to be obtained for a request (unless the param was overridden). The function
 *   will be passed the current data value as an argument.
 *
 *   Each key value in the parameter object is first bound to url template if present and then any
 *   excess keys are appended to the url search query after the `?`.
 *
 *   Given a template `/path/:verb` and parameter `{verb:'greet', salutation:'Hello'}` results in
 *   URL `/path/greet?salutation=Hello`.
 *
 *   If the parameter value is prefixed with `@`, then the value for that parameter will be
 *   extracted from the corresponding property on the `data` object (provided when calling a
 *   "non-GET" action method).
 *   For example, if the `defaultParam` object is `{someParam: '@someProp'}` then the value of
 *   `someParam` will be `data.someProp`.
 *   Note that the parameter will be ignored, when calling a "GET" action method (i.e. an action
 *   method that does not accept a request body)
 *
 * @param {Object.<Object>=} actions Hash with declaration of custom actions that should extend
 *   the default set of resource actions. The declaration should be created in the format of {@link
 *   ng.$http#usage $http.config}:
 *
 *       {action1: {method:?, params:?, isArray:?, headers:?, ...},
 *        action2: {method:?, params:?, isArray:?, headers:?, ...},
 *        ...}
 *
 *   Where:
 *
 *   - **`action`** – {string} – The name of action. This name becomes the name of the method on
 *     your resource object.
 *   - **`method`** – {string} – Case insensitive HTTP method (e.g. `GET`, `POST`, `PUT`,
 *     `DELETE`, `JSONP`, etc).
 *   - **`params`** – {Object=} – Optional set of pre-bound parameters for this action. If any of
 *     the parameter value is a function, it will be called every time when a param value needs to
 *     be obtained for a request (unless the param was overridden). The function will be passed the
 *     current data value as an argument.
 *   - **`url`** – {string} – action specific `url` override. The url templating is supported just
 *     like for the resource-level urls.
 *   - **`isArray`** – {boolean=} – If true then the returned object for this action is an array,
 *     see `returns` section.
 *   - **`transformRequest`** –
 *     `{function(data, headersGetter)|Array.<function(data, headersGetter)>}` –
 *     transform function or an array of such functions. The transform function takes the http
 *     request body and headers and returns its transformed (typically serialized) version.
 *     By default, transformRequest will contain one function that checks if the request data is
 *     an object and serializes to using `angular.toJson`. To prevent this behavior, set
 *     `transformRequest` to an empty array: `transformRequest: []`
 *   - **`transformResponse`** –
 *     `{function(data, headersGetter)|Array.<function(data, headersGetter)>}` –
 *     transform function or an array of such functions. The transform function takes the http
 *     response body and headers and returns its transformed (typically deserialized) version.
 *     By default, transformResponse will contain one function that checks if the response looks
 *     like a JSON string and deserializes it using `angular.fromJson`. To prevent this behavior,
 *     set `transformResponse` to an empty array: `transformResponse: []`
 *   - **`cache`** – `{boolean|Cache}` – If true, a default $http cache will be used to cache the
 *     GET request, otherwise if a cache instance built with
 *     {@link ng.$cacheFactory $cacheFactory}, this cache will be used for
 *     caching.
 *   - **`timeout`** – `{number}` – timeout in milliseconds.<br />
 *     **Note:** In contrast to {@link ng.$http#usage $http.config}, {@link ng.$q promises} are
 *     **not** supported in $resource, because the same value would be used for multiple requests.
 *     If you are looking for a way to cancel requests, you should use the `cancellable` option.
 *   - **`cancellable`** – `{boolean}` – if set to true, the request made by a "non-instance" call
 *     will be cancelled (if not already completed) by calling `$cancelRequest()` on the call's
 *     return value. Calling `$cancelRequest()` for a non-cancellable or an already
 *     completed/cancelled request will have no effect.<br />
 *   - **`withCredentials`** - `{boolean}` - whether to set the `withCredentials` flag on the
 *     XHR object. See
 *     [requests with credentials](https://developer.mozilla.org/en/http_access_control#section_5)
 *     for more information.
 *   - **`responseType`** - `{string}` - see
 *     [requestType](https://developer.mozilla.org/en-US/docs/DOM/XMLHttpRequest#responseType).
 *   - **`interceptor`** - `{Object=}` - The interceptor object has two optional methods -
 *     `response` and `responseError`. Both `response` and `responseError` interceptors get called
 *     with `http response` object. See {@link ng.$http $http interceptors}.
 *
 * @param {Object} options Hash with custom settings that should extend the
 *   default `$resourceProvider` behavior.  The supported options are:
 *
 *   - **`stripTrailingSlashes`** – {boolean} – If true then the trailing
 *   slashes from any calculated URL will be stripped. (Defaults to true.)
 *   - **`cancellable`** – {boolean} – If true, the request made by a "non-instance" call will be
 *   cancelled (if not already completed) by calling `$cancelRequest()` on the call's return value.
 *   This can be overwritten per action. (Defaults to false.)
 *
 * @returns {Object} A resource "class" object with methods for the default set of resource actions
 *   optionally extended with custom `actions`. The default set contains these actions:
 *   ```js
 *   { 'get':    {method:'GET'},
 *     'save':   {method:'POST'},
 *     'query':  {method:'GET', isArray:true},
 *     'remove': {method:'DELETE'},
 *     'delete': {method:'DELETE'} };
 *   ```
 *
 *   Calling these methods invoke an {@link ng.$http} with the specified http method,
 *   destination and parameters. When the data is returned from the server then the object is an
 *   instance of the resource class. The actions `save`, `remove` and `delete` are available on it
 *   as  methods with the `$` prefix. This allows you to easily perform CRUD operations (create,
 *   read, update, delete) on server-side data like this:
 *   ```js
 *   var User = $resource('/user/:userId', {userId:'@id'});
 *   var user = User.get({userId:123}, function() {
 *     user.abc = true;
 *     user.$save();
 *   });
 *   ```
 *
 *   It is important to realize that invoking a $resource object method immediately returns an
 *   empty reference (object or array depending on `isArray`). Once the data is returned from the
 *   server the existing reference is populated with the actual data. This is a useful trick since
 *   usually the resource is assigned to a model which is then rendered by the view. Having an empty
 *   object results in no rendering, once the data arrives from the server then the object is
 *   populated with the data and the view automatically re-renders itself showing the new data. This
 *   means that in most cases one never has to write a callback function for the action methods.
 *
 *   The action methods on the class object or instance object can be invoked with the following
 *   parameters:
 *
 *   - HTTP GET "class" actions: `Resource.action([parameters], [success], [error])`
 *   - non-GET "class" actions: `Resource.action([parameters], postData, [success], [error])`
 *   - non-GET instance actions:  `instance.$action([parameters], [success], [error])`
 *
 *
 *   Success callback is called with (value, responseHeaders) arguments, where the value is
 *   the populated resource instance or collection object. The error callback is called
 *   with (httpResponse) argument.
 *
 *   Class actions return empty instance (with additional properties below).
 *   Instance actions return promise of the action.
 *
 *   The Resource instances and collections have these additional properties:
 *
 *   - `$promise`: the {@link ng.$q promise} of the original server interaction that created this
 *     instance or collection.
 *
 *     On success, the promise is resolved with the same resource instance or collection object,
 *     updated with data from server. This makes it easy to use in
 *     {@link ngRoute.$routeProvider resolve section of $routeProvider.when()} to defer view
 *     rendering until the resource(s) are loaded.
 *
 *     On failure, the promise is rejected with the {@link ng.$http http response} object, without
 *     the `resource` property.
 *
 *     If an interceptor object was provided, the promise will instead be resolved with the value
 *     returned by the interceptor.
 *
 *   - `$resolved`: `true` after first server interaction is completed (either with success or
 *      rejection), `false` before that. Knowing if the Resource has been resolved is useful in
 *      data-binding.
 *
 *   The Resource instances and collections have these additional methods:
 *
 *   - `$cancelRequest`: If there is a cancellable, pending request related to the instance or
 *      collection, calling this method will abort the request.
 *
 *   The Resource instances have these additional methods:
 *
 *   - `toJSON`: It returns a simple object without any of the extra properties added as part of
 *     the Resource API. This object can be serialized through {@link angular.toJson} safely
 *     without attaching Angular-specific fields. Notice that `JSON.stringify` (and
 *     `angular.toJson`) automatically use this method when serializing a Resource instance
 *     (see [MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/JSON/stringify#toJSON()_behavior)).
 *
 * @example
 *
 * # Credit card resource
 *
 * ```js
     // Define CreditCard class
     var CreditCard = $resource('/user/:userId/card/:cardId',
      {userId:123, cardId:'@id'}, {
       charge: {method:'POST', params:{charge:true}}
      });

     // We can retrieve a collection from the server
     var cards = CreditCard.query(function() {
       // GET: /user/123/card
       // server returns: [ {id:456, number:'1234', name:'Smith'} ];

       var card = cards[0];
       // each item is an instance of CreditCard
       expect(card instanceof CreditCard).toEqual(true);
       card.name = "J. Smith";
       // non GET methods are mapped onto the instances
       card.$save();
       // POST: /user/123/card/456 {id:456, number:'1234', name:'J. Smith'}
       // server returns: {id:456, number:'1234', name: 'J. Smith'};

       // our custom method is mapped as well.
       card.$charge({amount:9.99});
       // POST: /user/123/card/456?amount=9.99&charge=true {id:456, number:'1234', name:'J. Smith'}
     });

     // we can create an instance as well
     var newCard = new CreditCard({number:'0123'});
     newCard.name = "Mike Smith";
     newCard.$save();
     // POST: /user/123/card {number:'0123', name:'Mike Smith'}
     // server returns: {id:789, number:'0123', name: 'Mike Smith'};
     expect(newCard.id).toEqual(789);
 * ```
 *
 * The object returned from this function execution is a resource "class" which has "static" method
 * for each action in the definition.
 *
 * Calling these methods invoke `$http` on the `url` template with the given `method`, `params` and
 * `headers`.
 *
 * @example
 *
 * # User resource
 *
 * When the data is returned from the server then the object is an instance of the resource type and
 * all of the non-GET methods are available with `$` prefix. This allows you to easily support CRUD
 * operations (create, read, update, delete) on server-side data.

   ```js
     var User = $resource('/user/:userId', {userId:'@id'});
     User.get({userId:123}, function(user) {
       user.abc = true;
       user.$save();
     });
   ```
 *
 * It's worth noting that the success callback for `get`, `query` and other methods gets passed
 * in the response that came from the server as well as $http header getter function, so one
 * could rewrite the above example and get access to http headers as:
 *
   ```js
     var User = $resource('/user/:userId', {userId:'@id'});
     User.get({userId:123}, function(user, getResponseHeaders){
       user.abc = true;
       user.$save(function(user, putResponseHeaders) {
         //user => saved user object
         //putResponseHeaders => $http header getter
       });
     });
   ```
 *
 * You can also access the raw `$http` promise via the `$promise` property on the object returned
 *
   ```
     var User = $resource('/user/:userId', {userId:'@id'});
     User.get({userId:123})
         .$promise.then(function(user) {
           $scope.user = user;
         });
   ```
 *
 * @example
 *
 * # Creating a custom 'PUT' request
 *
 * In this example we create a custom method on our resource to make a PUT request
 * ```js
 *    var app = angular.module('app', ['ngResource', 'ngRoute']);
 *
 *    // Some APIs expect a PUT request in the format URL/object/ID
 *    // Here we are creating an 'update' method
 *    app.factory('Notes', ['$resource', function($resource) {
 *    return $resource('/notes/:id', null,
 *        {
 *            'update': { method:'PUT' }
 *        });
 *    }]);
 *
 *    // In our controller we get the ID from the URL using ngRoute and $routeParams
 *    // We pass in $routeParams and our Notes factory along with $scope
 *    app.controller('NotesCtrl', ['$scope', '$routeParams', 'Notes',
                                      function($scope, $routeParams, Notes) {
 *    // First get a note object from the factory
 *    var note = Notes.get({ id:$routeParams.id });
 *    $id = note.id;
 *
 *    // Now call update passing in the ID first then the object you are updating
 *    Notes.update({ id:$id }, note);
 *
 *    // This will PUT /notes/ID with the note object in the request payload
 *    }]);
 * ```
 *
 * @example
 *
 * # Cancelling requests
 *
 * If an action's configuration specifies that it is cancellable, you can cancel the request related
 * to an instance or collection (as long as it is a result of a "non-instance" call):
 *
   ```js
     // ...defining the `Hotel` resource...
     var Hotel = $resource('/api/hotel/:id', {id: '@id'}, {
       // Let's make the `query()` method cancellable
       query: {method: 'get', isArray: true, cancellable: true}
     });

     // ...somewhere in the PlanVacationController...
     ...
     this.onDestinationChanged = function onDestinationChanged(destination) {
       // We don't care about any pending request for hotels
       // in a different destination any more
       this.availableHotels.$cancelRequest();

       // Let's query for hotels in '<destination>'
       // (calls: /api/hotel?location=<destination>)
       this.availableHotels = Hotel.query({location: destination});
     };
   ```
 *
 */
angular.module('ngResource', ['ng']).
  provider('$resource', function() {
    var PROTOCOL_AND_DOMAIN_REGEX = /^https?:\/\/[^\/]*/;
    var provider = this;

    /**
     * @ngdoc property
     * @name $resourceProvider#defaults
     * @description
     * Object containing default options used when creating `$resource` instances.
     *
     * The default values satisfy a wide range of usecases, but you may choose to overwrite any of
     * them to further customize your instances. The available properties are:
     *
     * - **stripTrailingSlashes** – `{boolean}` – If true, then the trailing slashes from any
     *   calculated URL will be stripped.<br />
     *   (Defaults to true.)
     * - **cancellable** – `{boolean}` – If true, the request made by a "non-instance" call will be
     *   cancelled (if not already completed) by calling `$cancelRequest()` on the call's return
     *   value. For more details, see {@link ngResource.$resource}. This can be overwritten per
     *   resource class or action.<br />
     *   (Defaults to false.)
     * - **actions** - `{Object.<Object>}` - A hash with default actions declarations. Actions are
     *   high-level methods corresponding to RESTful actions/methods on resources. An action may
     *   specify what HTTP method to use, what URL to hit, if the return value will be a single
     *   object or a collection (array) of objects etc. For more details, see
     *   {@link ngResource.$resource}. The actions can also be enhanced or overwritten per resource
     *   class.<br />
     *   The default actions are:
     *   ```js
     *   {
     *     get: {method: 'GET'},
     *     save: {method: 'POST'},
     *     query: {method: 'GET', isArray: true},
     *     remove: {method: 'DELETE'},
     *     delete: {method: 'DELETE'}
     *   }
     *   ```
     *
     * #### Example
     *
     * For example, you can specify a new `update` action that uses the `PUT` HTTP verb:
     *
     * ```js
     *   angular.
     *     module('myApp').
     *     config(['resourceProvider', function ($resourceProvider) {
     *       $resourceProvider.defaults.actions.update = {
     *         method: 'PUT'
     *       };
     *     });
     * ```
     *
     * Or you can even overwrite the whole `actions` list and specify your own:
     *
     * ```js
     *   angular.
     *     module('myApp').
     *     config(['resourceProvider', function ($resourceProvider) {
     *       $resourceProvider.defaults.actions = {
     *         create: {method: 'POST'}
     *         get:    {method: 'GET'},
     *         getAll: {method: 'GET', isArray:true},
     *         update: {method: 'PUT'},
     *         delete: {method: 'DELETE'}
     *       };
     *     });
     * ```
     *
     */
    this.defaults = {
      // Strip slashes by default
      stripTrailingSlashes: true,

      // Make non-instance requests cancellable (via `$cancelRequest()`)
      cancellable: false,

      // Default actions configuration
      actions: {
        'get': {method: 'GET'},
        'save': {method: 'POST'},
        'query': {method: 'GET', isArray: true},
        'remove': {method: 'DELETE'},
        'delete': {method: 'DELETE'}
      }
    };

    this.$get = ['$http', '$log', '$q', '$timeout', function($http, $log, $q, $timeout) {

      var noop = angular.noop,
        forEach = angular.forEach,
        extend = angular.extend,
        copy = angular.copy,
        isFunction = angular.isFunction;

      /**
       * We need our custom method because encodeURIComponent is too aggressive and doesn't follow
       * http://www.ietf.org/rfc/rfc3986.txt with regards to the character set
       * (pchar) allowed in path segments:
       *    segment       = *pchar
       *    pchar         = unreserved / pct-encoded / sub-delims / ":" / "@"
       *    pct-encoded   = "%" HEXDIG HEXDIG
       *    unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
       *    sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
       *                     / "*" / "+" / "," / ";" / "="
       */
      function encodeUriSegment(val) {
        return encodeUriQuery(val, true).
          replace(/%26/gi, '&').
          replace(/%3D/gi, '=').
          replace(/%2B/gi, '+');
      }


      /**
       * This method is intended for encoding *key* or *value* parts of query component. We need a
       * custom method because encodeURIComponent is too aggressive and encodes stuff that doesn't
       * have to be encoded per http://tools.ietf.org/html/rfc3986:
       *    query       = *( pchar / "/" / "?" )
       *    pchar         = unreserved / pct-encoded / sub-delims / ":" / "@"
       *    unreserved    = ALPHA / DIGIT / "-" / "." / "_" / "~"
       *    pct-encoded   = "%" HEXDIG HEXDIG
       *    sub-delims    = "!" / "$" / "&" / "'" / "(" / ")"
       *                     / "*" / "+" / "," / ";" / "="
       */
      function encodeUriQuery(val, pctEncodeSpaces) {
        return encodeURIComponent(val).
          replace(/%40/gi, '@').
          replace(/%3A/gi, ':').
          replace(/%24/g, '$').
          replace(/%2C/gi, ',').
          replace(/%20/g, (pctEncodeSpaces ? '%20' : '+'));
      }

      function Route(template, defaults) {
        this.template = template;
        this.defaults = extend({}, provider.defaults, defaults);
        this.urlParams = {};
      }

      Route.prototype = {
        setUrlParams: function(config, params, actionUrl) {
          var self = this,
            url = actionUrl || self.template,
            val,
            encodedVal,
            protocolAndDomain = '';

          var urlParams = self.urlParams = {};
          forEach(url.split(/\W/), function(param) {
            if (param === 'hasOwnProperty') {
              throw $resourceMinErr('badname', "hasOwnProperty is not a valid parameter name.");
            }
            if (!(new RegExp("^\\d+$").test(param)) && param &&
              (new RegExp("(^|[^\\\\]):" + param + "(\\W|$)").test(url))) {
              urlParams[param] = {
                isQueryParamValue: (new RegExp("\\?.*=:" + param + "(?:\\W|$)")).test(url)
              };
            }
          });
          url = url.replace(/\\:/g, ':');
          url = url.replace(PROTOCOL_AND_DOMAIN_REGEX, function(match) {
            protocolAndDomain = match;
            return '';
          });

          params = params || {};
          forEach(self.urlParams, function(paramInfo, urlParam) {
            val = params.hasOwnProperty(urlParam) ? params[urlParam] : self.defaults[urlParam];
            if (angular.isDefined(val) && val !== null) {
              if (paramInfo.isQueryParamValue) {
                encodedVal = encodeUriQuery(val, true);
              } else {
                encodedVal = encodeUriSegment(val);
              }
              url = url.replace(new RegExp(":" + urlParam + "(\\W|$)", "g"), function(match, p1) {
                return encodedVal + p1;
              });
            } else {
              url = url.replace(new RegExp("(\/?):" + urlParam + "(\\W|$)", "g"), function(match,
                  leadingSlashes, tail) {
                if (tail.charAt(0) == '/') {
                  return tail;
                } else {
                  return leadingSlashes + tail;
                }
              });
            }
          });

          // strip trailing slashes and set the url (unless this behavior is specifically disabled)
          if (self.defaults.stripTrailingSlashes) {
            url = url.replace(/\/+$/, '') || '/';
          }

          // then replace collapse `/.` if found in the last URL path segment before the query
          // E.g. `http://url.com/id./format?q=x` becomes `http://url.com/id.format?q=x`
          url = url.replace(/\/\.(?=\w+($|\?))/, '.');
          // replace escaped `/\.` with `/.`
          config.url = protocolAndDomain + url.replace(/\/\\\./, '/.');


          // set params - delegate param encoding to $http
          forEach(params, function(value, key) {
            if (!self.urlParams[key]) {
              config.params = config.params || {};
              config.params[key] = value;
            }
          });
        }
      };


      function resourceFactory(url, paramDefaults, actions, options) {
        var route = new Route(url, options);

        actions = extend({}, provider.defaults.actions, actions);

        function extractParams(data, actionParams) {
          var ids = {};
          actionParams = extend({}, paramDefaults, actionParams);
          forEach(actionParams, function(value, key) {
            if (isFunction(value)) { value = value(data); }
            ids[key] = value && value.charAt && value.charAt(0) == '@' ?
              lookupDottedPath(data, value.substr(1)) : value;
          });
          return ids;
        }

        function defaultResponseInterceptor(response) {
          return response.resource;
        }

        function Resource(value) {
          shallowClearAndCopy(value || {}, this);
        }

        Resource.prototype.toJSON = function() {
          var data = extend({}, this);
          delete data.$promise;
          delete data.$resolved;
          return data;
        };

        forEach(actions, function(action, name) {
          var hasBody = /^(POST|PUT|PATCH)$/i.test(action.method);
          var numericTimeout = action.timeout;
          var cancellable = angular.isDefined(action.cancellable) ? action.cancellable :
              (options && angular.isDefined(options.cancellable)) ? options.cancellable :
              provider.defaults.cancellable;

          if (numericTimeout && !angular.isNumber(numericTimeout)) {
            $log.debug('ngResource:\n' +
                       '  Only numeric values are allowed as `timeout`.\n' +
                       '  Promises are not supported in $resource, because the same value would ' +
                       'be used for multiple requests. If you are looking for a way to cancel ' +
                       'requests, you should use the `cancellable` option.');
            delete action.timeout;
            numericTimeout = null;
          }

          Resource[name] = function(a1, a2, a3, a4) {
            var params = {}, data, success, error;

            /* jshint -W086 */ /* (purposefully fall through case statements) */
            switch (arguments.length) {
              case 4:
                error = a4;
                success = a3;
              //fallthrough
              case 3:
              case 2:
                if (isFunction(a2)) {
                  if (isFunction(a1)) {
                    success = a1;
                    error = a2;
                    break;
                  }

                  success = a2;
                  error = a3;
                  //fallthrough
                } else {
                  params = a1;
                  data = a2;
                  success = a3;
                  break;
                }
              case 1:
                if (isFunction(a1)) success = a1;
                else if (hasBody) data = a1;
                else params = a1;
                break;
              case 0: break;
              default:
                throw $resourceMinErr('badargs',
                  "Expected up to 4 arguments [params, data, success, error], got {0} arguments",
                  arguments.length);
            }
            /* jshint +W086 */ /* (purposefully fall through case statements) */

            var isInstanceCall = this instanceof Resource;
            var value = isInstanceCall ? data : (action.isArray ? [] : new Resource(data));
            var httpConfig = {};
            var responseInterceptor = action.interceptor && action.interceptor.response ||
              defaultResponseInterceptor;
            var responseErrorInterceptor = action.interceptor && action.interceptor.responseError ||
              undefined;
            var timeoutDeferred;
            var numericTimeoutPromise;

            forEach(action, function(value, key) {
              switch (key) {
                default:
                  httpConfig[key] = copy(value);
                  break;
                case 'params':
                case 'isArray':
                case 'interceptor':
                case 'cancellable':
                  break;
              }
            });

            if (!isInstanceCall && cancellable) {
              timeoutDeferred = $q.defer();
              httpConfig.timeout = timeoutDeferred.promise;

              if (numericTimeout) {
                numericTimeoutPromise = $timeout(timeoutDeferred.resolve, numericTimeout);
              }
            }

            if (hasBody) httpConfig.data = data;
            route.setUrlParams(httpConfig,
              extend({}, extractParams(data, action.params || {}), params),
              action.url);

            var promise = $http(httpConfig).then(function(response) {
              var data = response.data;

              if (data) {
                // Need to convert action.isArray to boolean in case it is undefined
                // jshint -W018
                if (angular.isArray(data) !== (!!action.isArray)) {
                  throw $resourceMinErr('badcfg',
                      'Error in resource configuration for action `{0}`. Expected response to ' +
                      'contain an {1} but got an {2} (Request: {3} {4})', name, action.isArray ? 'array' : 'object',
                    angular.isArray(data) ? 'array' : 'object', httpConfig.method, httpConfig.url);
                }
                // jshint +W018
                if (action.isArray) {
                  value.length = 0;
                  forEach(data, function(item) {
                    if (typeof item === "object") {
                      value.push(new Resource(item));
                    } else {
                      // Valid JSON values may be string literals, and these should not be converted
                      // into objects. These items will not have access to the Resource prototype
                      // methods, but unfortunately there
                      value.push(item);
                    }
                  });
                } else {
                  var promise = value.$promise;     // Save the promise
                  shallowClearAndCopy(data, value);
                  value.$promise = promise;         // Restore the promise
                }
              }
              response.resource = value;

              return response;
            }, function(response) {
              (error || noop)(response);
              return $q.reject(response);
            });

            promise['finally'](function() {
              value.$resolved = true;
              if (!isInstanceCall && cancellable) {
                value.$cancelRequest = angular.noop;
                $timeout.cancel(numericTimeoutPromise);
                timeoutDeferred = numericTimeoutPromise = httpConfig.timeout = null;
              }
            });

            promise = promise.then(
              function(response) {
                var value = responseInterceptor(response);
                (success || noop)(value, response.headers);
                return value;
              },
              responseErrorInterceptor);

            if (!isInstanceCall) {
              // we are creating instance / collection
              // - set the initial promise
              // - return the instance / collection
              value.$promise = promise;
              value.$resolved = false;
              if (cancellable) value.$cancelRequest = timeoutDeferred.resolve;

              return value;
            }

            // instance call
            return promise;
          };


          Resource.prototype['$' + name] = function(params, success, error) {
            if (isFunction(params)) {
              error = success; success = params; params = {};
            }
            var result = Resource[name].call(this, params, this, success, error);
            return result.$promise || result;
          };
        });

        Resource.bind = function(additionalParamDefaults) {
          return resourceFactory(url, extend({}, paramDefaults, additionalParamDefaults), actions);
        };

        return Resource;
      }

      return resourceFactory;
    }];
  });


})(window, window.angular);
;/*!
 * angular-translate - v2.11.1 - 2016-07-17
 * 
 * Copyright (c) 2016 The angular-translate team, Pascal Precht; Licensed MIT
 */
(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module unless amdModuleId is set
    define([], function () {
      return (factory());
    });
  } else if (typeof exports === 'object') {
    // Node. Does not work with strict CommonJS, but
    // only CommonJS-like environments that support module.exports,
    // like Node.
    module.exports = factory();
  } else {
    factory();
  }
}(this, function () {

/**
 * @ngdoc overview
 * @name pascalprecht.translate
 *
 * @description
 * The main module which holds everything together.
 */
runTranslate.$inject = ['$translate'];
$translate.$inject = ['$STORAGE_KEY', '$windowProvider', '$translateSanitizationProvider', 'pascalprechtTranslateOverrider'];
$translateDefaultInterpolation.$inject = ['$interpolate', '$translateSanitization'];
translateDirective.$inject = ['$translate', '$q', '$interpolate', '$compile', '$parse', '$rootScope'];
translateCloakDirective.$inject = ['$translate', '$rootScope'];
translateFilterFactory.$inject = ['$parse', '$translate'];
$translationCache.$inject = ['$cacheFactory'];
angular.module('pascalprecht.translate', ['ng'])
  .run(runTranslate);

function runTranslate($translate) {

  'use strict';

  var key = $translate.storageKey(),
    storage = $translate.storage();

  var fallbackFromIncorrectStorageValue = function () {
    var preferred = $translate.preferredLanguage();
    if (angular.isString(preferred)) {
      $translate.use(preferred);
      // $translate.use() will also remember the language.
      // So, we don't need to call storage.put() here.
    } else {
      storage.put(key, $translate.use());
    }
  };

  fallbackFromIncorrectStorageValue.displayName = 'fallbackFromIncorrectStorageValue';

  if (storage) {
    if (!storage.get(key)) {
      fallbackFromIncorrectStorageValue();
    } else {
      $translate.use(storage.get(key))['catch'](fallbackFromIncorrectStorageValue);
    }
  } else if (angular.isString($translate.preferredLanguage())) {
    $translate.use($translate.preferredLanguage());
  }
}

runTranslate.displayName = 'runTranslate';

/**
 * @ngdoc object
 * @name pascalprecht.translate.$translateSanitizationProvider
 *
 * @description
 *
 * Configurations for $translateSanitization
 */
angular.module('pascalprecht.translate').provider('$translateSanitization', $translateSanitizationProvider);

function $translateSanitizationProvider () {

  'use strict';

  var $sanitize,
      currentStrategy = null, // TODO change to either 'sanitize', 'escape' or ['sanitize', 'escapeParameters'] in 3.0.
      hasConfiguredStrategy = false,
      hasShownNoStrategyConfiguredWarning = false,
      strategies;

  /**
   * Definition of a sanitization strategy function
   * @callback StrategyFunction
   * @param {string|object} value - value to be sanitized (either a string or an interpolated value map)
   * @param {string} mode - either 'text' for a string (translation) or 'params' for the interpolated params
   * @return {string|object}
   */

  /**
   * @ngdoc property
   * @name strategies
   * @propertyOf pascalprecht.translate.$translateSanitizationProvider
   *
   * @description
   * Following strategies are built-in:
   * <dl>
   *   <dt>sanitize</dt>
   *   <dd>Sanitizes HTML in the translation text using $sanitize</dd>
   *   <dt>escape</dt>
   *   <dd>Escapes HTML in the translation</dd>
   *   <dt>sanitizeParameters</dt>
   *   <dd>Sanitizes HTML in the values of the interpolation parameters using $sanitize</dd>
   *   <dt>escapeParameters</dt>
   *   <dd>Escapes HTML in the values of the interpolation parameters</dd>
   *   <dt>escaped</dt>
   *   <dd>Support legacy strategy name 'escaped' for backwards compatibility (will be removed in 3.0)</dd>
   * </dl>
   *
   */

  strategies = {
    sanitize: function (value, mode) {
      if (mode === 'text') {
        value = htmlSanitizeValue(value);
      }
      return value;
    },
    escape: function (value, mode) {
      if (mode === 'text') {
        value = htmlEscapeValue(value);
      }
      return value;
    },
    sanitizeParameters: function (value, mode) {
      if (mode === 'params') {
        value = mapInterpolationParameters(value, htmlSanitizeValue);
      }
      return value;
    },
    escapeParameters: function (value, mode) {
      if (mode === 'params') {
        value = mapInterpolationParameters(value, htmlEscapeValue);
      }
      return value;
    }
  };
  // Support legacy strategy name 'escaped' for backwards compatibility.
  // TODO should be removed in 3.0
  strategies.escaped = strategies.escapeParameters;

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateSanitizationProvider#addStrategy
   * @methodOf pascalprecht.translate.$translateSanitizationProvider
   *
   * @description
   * Adds a sanitization strategy to the list of known strategies.
   *
   * @param {string} strategyName - unique key for a strategy
   * @param {StrategyFunction} strategyFunction - strategy function
   * @returns {object} this
   */
  this.addStrategy = function (strategyName, strategyFunction) {
    strategies[strategyName] = strategyFunction;
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateSanitizationProvider#removeStrategy
   * @methodOf pascalprecht.translate.$translateSanitizationProvider
   *
   * @description
   * Removes a sanitization strategy from the list of known strategies.
   *
   * @param {string} strategyName - unique key for a strategy
   * @returns {object} this
   */
  this.removeStrategy = function (strategyName) {
    delete strategies[strategyName];
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateSanitizationProvider#useStrategy
   * @methodOf pascalprecht.translate.$translateSanitizationProvider
   *
   * @description
   * Selects a sanitization strategy. When an array is provided the strategies will be executed in order.
   *
   * @param {string|StrategyFunction|array} strategy The sanitization strategy / strategies which should be used. Either a name of an existing strategy, a custom strategy function, or an array consisting of multiple names and / or custom functions.
   * @returns {object} this
   */
  this.useStrategy = function (strategy) {
    hasConfiguredStrategy = true;
    currentStrategy = strategy;
    return this;
  };

  /**
   * @ngdoc object
   * @name pascalprecht.translate.$translateSanitization
   * @requires $injector
   * @requires $log
   *
   * @description
   * Sanitizes interpolation parameters and translated texts.
   *
   */
  this.$get = ['$injector', '$log', function ($injector, $log) {

    var cachedStrategyMap = {};

    var applyStrategies = function (value, mode, selectedStrategies) {
      angular.forEach(selectedStrategies, function (selectedStrategy) {
        if (angular.isFunction(selectedStrategy)) {
          value = selectedStrategy(value, mode);
        } else if (angular.isFunction(strategies[selectedStrategy])) {
          value = strategies[selectedStrategy](value, mode);
        } else if (angular.isString(strategies[selectedStrategy])) {
          if (!cachedStrategyMap[strategies[selectedStrategy]]) {
            try {
              cachedStrategyMap[strategies[selectedStrategy]] = $injector.get(strategies[selectedStrategy]);
            } catch (e) {
              cachedStrategyMap[strategies[selectedStrategy]] = function() {};
              throw new Error('pascalprecht.translate.$translateSanitization: Unknown sanitization strategy: \'' + selectedStrategy + '\'');
            }
          }
          value = cachedStrategyMap[strategies[selectedStrategy]](value, mode);
        } else {
          throw new Error('pascalprecht.translate.$translateSanitization: Unknown sanitization strategy: \'' + selectedStrategy + '\'');
        }
      });
      return value;
    };

    // TODO: should be removed in 3.0
    var showNoStrategyConfiguredWarning = function () {
      if (!hasConfiguredStrategy && !hasShownNoStrategyConfiguredWarning) {
        $log.warn('pascalprecht.translate.$translateSanitization: No sanitization strategy has been configured. This can have serious security implications. See http://angular-translate.github.io/docs/#/guide/19_security for details.');
        hasShownNoStrategyConfiguredWarning = true;
      }
    };

    if ($injector.has('$sanitize')) {
      $sanitize = $injector.get('$sanitize');
    }

    return {
      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translateSanitization#useStrategy
       * @methodOf pascalprecht.translate.$translateSanitization
       *
       * @description
       * Selects a sanitization strategy. When an array is provided the strategies will be executed in order.
       *
       * @param {string|StrategyFunction|array} strategy The sanitization strategy / strategies which should be used. Either a name of an existing strategy, a custom strategy function, or an array consisting of multiple names and / or custom functions.
       */
      useStrategy: (function (self) {
        return function (strategy) {
          self.useStrategy(strategy);
        };
      })(this),

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translateSanitization#sanitize
       * @methodOf pascalprecht.translate.$translateSanitization
       *
       * @description
       * Sanitizes a value.
       *
       * @param {string|object} value The value which should be sanitized.
       * @param {string} mode The current sanitization mode, either 'params' or 'text'.
       * @param {string|StrategyFunction|array} [strategy] Optional custom strategy which should be used instead of the currently selected strategy.
       * @returns {string|object} sanitized value
       */
      sanitize: function (value, mode, strategy) {
        if (!currentStrategy) {
          showNoStrategyConfiguredWarning();
        }

        if (arguments.length < 3) {
          strategy = currentStrategy;
        }

        if (!strategy) {
          return value;
        }

        var selectedStrategies = angular.isArray(strategy) ? strategy : [strategy];
        return applyStrategies(value, mode, selectedStrategies);
      }
    };
  }];

  var htmlEscapeValue = function (value) {
    var element = angular.element('<div></div>');
    element.text(value); // not chainable, see #1044
    return element.html();
  };

  var htmlSanitizeValue = function (value) {
    if (!$sanitize) {
      throw new Error('pascalprecht.translate.$translateSanitization: Error cannot find $sanitize service. Either include the ngSanitize module (https://docs.angularjs.org/api/ngSanitize) or use a sanitization strategy which does not depend on $sanitize, such as \'escape\'.');
    }
    return $sanitize(value);
  };

  var mapInterpolationParameters = function (value, iteratee, stack) {
    if (angular.isObject(value)) {
      var result = angular.isArray(value) ? [] : {};

      if (!stack) {
        stack = [];
      } else {
        if (stack.indexOf(value) > -1) {
          throw new Error('pascalprecht.translate.$translateSanitization: Error cannot interpolate parameter due recursive object');
        }
      }

      stack.push(value);
      angular.forEach(value, function (propertyValue, propertyKey) {

        /* Skipping function properties. */
        if (angular.isFunction(propertyValue)) {
          return;
        }

        result[propertyKey] = mapInterpolationParameters(propertyValue, iteratee, stack);
      });
      stack.splice(-1, 1); // remove last

      return result;
    } else if (angular.isNumber(value)) {
      return value;
    } else {
      return iteratee(value);
    }
  };
}

/**
 * @ngdoc object
 * @name pascalprecht.translate.$translateProvider
 * @description
 *
 * $translateProvider allows developers to register translation-tables, asynchronous loaders
 * and similar to configure translation behavior directly inside of a module.
 *
 */
angular.module('pascalprecht.translate')
.constant('pascalprechtTranslateOverrider', {})
.provider('$translate', $translate);

function $translate($STORAGE_KEY, $windowProvider, $translateSanitizationProvider, pascalprechtTranslateOverrider) {

  'use strict';

  var $translationTable = {},
      $preferredLanguage,
      $availableLanguageKeys = [],
      $languageKeyAliases,
      $fallbackLanguage,
      $fallbackWasString,
      $uses,
      $nextLang,
      $storageFactory,
      $storageKey = $STORAGE_KEY,
      $storagePrefix,
      $missingTranslationHandlerFactory,
      $interpolationFactory,
      $interpolatorFactories = [],
      $loaderFactory,
      $cloakClassName = 'translate-cloak',
      $loaderOptions,
      $notFoundIndicatorLeft,
      $notFoundIndicatorRight,
      $postCompilingEnabled = false,
      $forceAsyncReloadEnabled = false,
      $nestedObjectDelimeter = '.',
      $isReady = false,
      $keepContent = false,
      loaderCache,
      directivePriority = 0,
      statefulFilter = true,
      postProcessFn,
      uniformLanguageTagResolver = 'default',
      languageTagResolver = {
        'default': function (tag) {
          return (tag || '').split('-').join('_');
        },
        java: function (tag) {
          var temp = (tag || '').split('-').join('_');
          var parts = temp.split('_');
          return parts.length > 1 ? (parts[0].toLowerCase() + '_' + parts[1].toUpperCase()) : temp;
        },
        bcp47: function (tag) {
          var temp = (tag || '').split('_').join('-');
          var parts = temp.split('-');
          return parts.length > 1 ? (parts[0].toLowerCase() + '-' + parts[1].toUpperCase()) : temp;
        },
        'iso639-1': function (tag) {
          var temp = (tag || '').split('_').join('-');
          var parts = temp.split('-');
          return parts[0].toLowerCase();
        }
      };

  var version = '2.11.1';

  // tries to determine the browsers language
  var getFirstBrowserLanguage = function () {

    // internal purpose only
    if (angular.isFunction(pascalprechtTranslateOverrider.getLocale)) {
      return pascalprechtTranslateOverrider.getLocale();
    }

    var nav = $windowProvider.$get().navigator,
        browserLanguagePropertyKeys = ['language', 'browserLanguage', 'systemLanguage', 'userLanguage'],
        i,
        language;

    // support for HTML 5.1 "navigator.languages"
    if (angular.isArray(nav.languages)) {
      for (i = 0; i < nav.languages.length; i++) {
        language = nav.languages[i];
        if (language && language.length) {
          return language;
        }
      }
    }

    // support for other well known properties in browsers
    for (i = 0; i < browserLanguagePropertyKeys.length; i++) {
      language = nav[browserLanguagePropertyKeys[i]];
      if (language && language.length) {
        return language;
      }
    }

    return null;
  };
  getFirstBrowserLanguage.displayName = 'angular-translate/service: getFirstBrowserLanguage';

  // tries to determine the browsers locale
  var getLocale = function () {
    var locale = getFirstBrowserLanguage() || '';
    if (languageTagResolver[uniformLanguageTagResolver]) {
      locale = languageTagResolver[uniformLanguageTagResolver](locale);
    }
    return locale;
  };
  getLocale.displayName = 'angular-translate/service: getLocale';

  /**
   * @name indexOf
   * @private
   *
   * @description
   * indexOf polyfill. Kinda sorta.
   *
   * @param {array} array Array to search in.
   * @param {string} searchElement Element to search for.
   *
   * @returns {int} Index of search element.
   */
  var indexOf = function(array, searchElement) {
    for (var i = 0, len = array.length; i < len; i++) {
      if (array[i] === searchElement) {
        return i;
      }
    }
    return -1;
  };

  /**
   * @name trim
   * @private
   *
   * @description
   * trim polyfill
   *
   * @returns {string} The string stripped of whitespace from both ends
   */
  var trim = function() {
    return this.toString().replace(/^\s+|\s+$/g, '');
  };

  var negotiateLocale = function (preferred) {
    if(!preferred) {
      return;
    }

    var avail = [],
        locale = angular.lowercase(preferred),
        i = 0,
        n = $availableLanguageKeys.length;

    for (; i < n; i++) {
      avail.push(angular.lowercase($availableLanguageKeys[i]));
    }

    // Check for an exact match in our list of available keys
    if (indexOf(avail, locale) > -1) {
      return preferred;
    }

    if ($languageKeyAliases) {
      var alias;
      for (var langKeyAlias in $languageKeyAliases) {
        if ($languageKeyAliases.hasOwnProperty(langKeyAlias)) {
          var hasWildcardKey = false;
          var hasExactKey = Object.prototype.hasOwnProperty.call($languageKeyAliases, langKeyAlias) &&
            angular.lowercase(langKeyAlias) === angular.lowercase(preferred);

          if (langKeyAlias.slice(-1) === '*') {
            hasWildcardKey = langKeyAlias.slice(0, -1) === preferred.slice(0, langKeyAlias.length - 1);
          }
          if (hasExactKey || hasWildcardKey) {
            alias = $languageKeyAliases[langKeyAlias];
            if (indexOf(avail, angular.lowercase(alias)) > -1) {
              return alias;
            }
          }
        }
      }
    }

    // Check for a language code without region
    var parts = preferred.split('_');

    if (parts.length > 1 && indexOf(avail, angular.lowercase(parts[0])) > -1) {
      return parts[0];
    }

    // If everything fails, return undefined.
    return;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#translations
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Registers a new translation table for specific language key.
   *
   * To register a translation table for specific language, pass a defined language
   * key as first parameter.
   *
   * <pre>
   *  // register translation table for language: 'de_DE'
   *  $translateProvider.translations('de_DE', {
   *    'GREETING': 'Hallo Welt!'
   *  });
   *
   *  // register another one
   *  $translateProvider.translations('en_US', {
   *    'GREETING': 'Hello world!'
   *  });
   * </pre>
   *
   * When registering multiple translation tables for for the same language key,
   * the actual translation table gets extended. This allows you to define module
   * specific translation which only get added, once a specific module is loaded in
   * your app.
   *
   * Invoking this method with no arguments returns the translation table which was
   * registered with no language key. Invoking it with a language key returns the
   * related translation table.
   *
   * @param {string} langKey A language key.
   * @param {object} translationTable A plain old JavaScript object that represents a translation table.
   *
   */
  var translations = function (langKey, translationTable) {

    if (!langKey && !translationTable) {
      return $translationTable;
    }

    if (langKey && !translationTable) {
      if (angular.isString(langKey)) {
        return $translationTable[langKey];
      }
    } else {
      if (!angular.isObject($translationTable[langKey])) {
        $translationTable[langKey] = {};
      }
      angular.extend($translationTable[langKey], flatObject(translationTable));
    }
    return this;
  };

  this.translations = translations;

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#cloakClassName
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   *
   * Let's you change the class name for `translate-cloak` directive.
   * Default class name is `translate-cloak`.
   *
   * @param {string} name translate-cloak class name
   */
  this.cloakClassName = function (name) {
    if (!name) {
      return $cloakClassName;
    }
    $cloakClassName = name;
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#nestedObjectDelimeter
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   *
   * Let's you change the delimiter for namespaced translations.
   * Default delimiter is `.`.
   *
   * @param {string} delimiter namespace separator
   */
  this.nestedObjectDelimeter = function (delimiter) {
    if (!delimiter) {
      return $nestedObjectDelimeter;
    }
    $nestedObjectDelimeter = delimiter;
    return this;
  };

  /**
   * @name flatObject
   * @private
   *
   * @description
   * Flats an object. This function is used to flatten given translation data with
   * namespaces, so they are later accessible via dot notation.
   */
  var flatObject = function (data, path, result, prevKey) {
    var key, keyWithPath, keyWithShortPath, val;

    if (!path) {
      path = [];
    }
    if (!result) {
      result = {};
    }
    for (key in data) {
      if (!Object.prototype.hasOwnProperty.call(data, key)) {
        continue;
      }
      val = data[key];
      if (angular.isObject(val)) {
        flatObject(val, path.concat(key), result, key);
      } else {
        keyWithPath = path.length ? ('' + path.join($nestedObjectDelimeter) + $nestedObjectDelimeter + key) : key;
        if(path.length && key === prevKey){
          // Create shortcut path (foo.bar == foo.bar.bar)
          keyWithShortPath = '' + path.join($nestedObjectDelimeter);
          // Link it to original path
          result[keyWithShortPath] = '@:' + keyWithPath;
        }
        result[keyWithPath] = val;
      }
    }
    return result;
  };
  flatObject.displayName = 'flatObject';

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#addInterpolation
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Adds interpolation services to angular-translate, so it can manage them.
   *
   * @param {object} factory Interpolation service factory
   */
  this.addInterpolation = function (factory) {
    $interpolatorFactories.push(factory);
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useMessageFormatInterpolation
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells angular-translate to use interpolation functionality of messageformat.js.
   * This is useful when having high level pluralization and gender selection.
   */
  this.useMessageFormatInterpolation = function () {
    return this.useInterpolation('$translateMessageFormatInterpolation');
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useInterpolation
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells angular-translate which interpolation style to use as default, application-wide.
   * Simply pass a factory/service name. The interpolation service has to implement
   * the correct interface.
   *
   * @param {string} factory Interpolation service name.
   */
  this.useInterpolation = function (factory) {
    $interpolationFactory = factory;
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useSanitizeStrategy
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Simply sets a sanitation strategy type.
   *
   * @param {string} value Strategy type.
   */
  this.useSanitizeValueStrategy = function (value) {
    $translateSanitizationProvider.useStrategy(value);
    return this;
  };

 /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#preferredLanguage
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells the module which of the registered translation tables to use for translation
   * at initial startup by passing a language key. Similar to `$translateProvider#use`
   * only that it says which language to **prefer**.
   *
   * @param {string} langKey A language key.
   */
  this.preferredLanguage = function(langKey) {
    if (langKey) {
      setupPreferredLanguage(langKey);
      return this;
    }
    return $preferredLanguage;
  };
  var setupPreferredLanguage = function (langKey) {
    if (langKey) {
      $preferredLanguage = langKey;
    }
    return $preferredLanguage;
  };
  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#translationNotFoundIndicator
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Sets an indicator which is used when a translation isn't found. E.g. when
   * setting the indicator as 'X' and one tries to translate a translation id
   * called `NOT_FOUND`, this will result in `X NOT_FOUND X`.
   *
   * Internally this methods sets a left indicator and a right indicator using
   * `$translateProvider.translationNotFoundIndicatorLeft()` and
   * `$translateProvider.translationNotFoundIndicatorRight()`.
   *
   * **Note**: These methods automatically add a whitespace between the indicators
   * and the translation id.
   *
   * @param {string} indicator An indicator, could be any string.
   */
  this.translationNotFoundIndicator = function (indicator) {
    this.translationNotFoundIndicatorLeft(indicator);
    this.translationNotFoundIndicatorRight(indicator);
    return this;
  };

  /**
   * ngdoc function
   * @name pascalprecht.translate.$translateProvider#translationNotFoundIndicatorLeft
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Sets an indicator which is used when a translation isn't found left to the
   * translation id.
   *
   * @param {string} indicator An indicator.
   */
  this.translationNotFoundIndicatorLeft = function (indicator) {
    if (!indicator) {
      return $notFoundIndicatorLeft;
    }
    $notFoundIndicatorLeft = indicator;
    return this;
  };

  /**
   * ngdoc function
   * @name pascalprecht.translate.$translateProvider#translationNotFoundIndicatorLeft
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Sets an indicator which is used when a translation isn't found right to the
   * translation id.
   *
   * @param {string} indicator An indicator.
   */
  this.translationNotFoundIndicatorRight = function (indicator) {
    if (!indicator) {
      return $notFoundIndicatorRight;
    }
    $notFoundIndicatorRight = indicator;
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#fallbackLanguage
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells the module which of the registered translation tables to use when missing translations
   * at initial startup by passing a language key. Similar to `$translateProvider#use`
   * only that it says which language to **fallback**.
   *
   * @param {string||array} langKey A language key.
   *
   */
  this.fallbackLanguage = function (langKey) {
    fallbackStack(langKey);
    return this;
  };

  var fallbackStack = function (langKey) {
    if (langKey) {
      if (angular.isString(langKey)) {
        $fallbackWasString = true;
        $fallbackLanguage = [ langKey ];
      } else if (angular.isArray(langKey)) {
        $fallbackWasString = false;
        $fallbackLanguage = langKey;
      }
      if (angular.isString($preferredLanguage)  && indexOf($fallbackLanguage, $preferredLanguage) < 0) {
        $fallbackLanguage.push($preferredLanguage);
      }

      return this;
    } else {
      if ($fallbackWasString) {
        return $fallbackLanguage[0];
      } else {
        return $fallbackLanguage;
      }
    }
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#use
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Set which translation table to use for translation by given language key. When
   * trying to 'use' a language which isn't provided, it'll throw an error.
   *
   * You actually don't have to use this method since `$translateProvider#preferredLanguage`
   * does the job too.
   *
   * @param {string} langKey A language key.
   */
  this.use = function (langKey) {
    if (langKey) {
      if (!$translationTable[langKey] && (!$loaderFactory)) {
        // only throw an error, when not loading translation data asynchronously
        throw new Error('$translateProvider couldn\'t find translationTable for langKey: \'' + langKey + '\'');
      }
      $uses = langKey;
      return this;
    }
    return $uses;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#resolveClientLocale
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * This returns the current browser/client's language key. The result is processed with the configured uniform tag resolver.
   *
   * @returns {string} the current client/browser language key
   */
  this.resolveClientLocale = function () {
    return getLocale();
  };

 /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#storageKey
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells the module which key must represent the choosed language by a user in the storage.
   *
   * @param {string} key A key for the storage.
   */
  var storageKey = function(key) {
    if (!key) {
      if ($storagePrefix) {
        return $storagePrefix + $storageKey;
      }
      return $storageKey;
    }
    $storageKey = key;
    return this;
  };

  this.storageKey = storageKey;

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useUrlLoader
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells angular-translate to use `$translateUrlLoader` extension service as loader.
   *
   * @param {string} url Url
   * @param {Object=} options Optional configuration object
   */
  this.useUrlLoader = function (url, options) {
    return this.useLoader('$translateUrlLoader', angular.extend({ url: url }, options));
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useStaticFilesLoader
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells angular-translate to use `$translateStaticFilesLoader` extension service as loader.
   *
   * @param {Object=} options Optional configuration object
   */
  this.useStaticFilesLoader = function (options) {
    return this.useLoader('$translateStaticFilesLoader', options);
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useLoader
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells angular-translate to use any other service as loader.
   *
   * @param {string} loaderFactory Factory name to use
   * @param {Object=} options Optional configuration object
   */
  this.useLoader = function (loaderFactory, options) {
    $loaderFactory = loaderFactory;
    $loaderOptions = options || {};
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useLocalStorage
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells angular-translate to use `$translateLocalStorage` service as storage layer.
   *
   */
  this.useLocalStorage = function () {
    return this.useStorage('$translateLocalStorage');
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useCookieStorage
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells angular-translate to use `$translateCookieStorage` service as storage layer.
   */
  this.useCookieStorage = function () {
    return this.useStorage('$translateCookieStorage');
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useStorage
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells angular-translate to use custom service as storage layer.
   */
  this.useStorage = function (storageFactory) {
    $storageFactory = storageFactory;
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#storagePrefix
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Sets prefix for storage key.
   *
   * @param {string} prefix Storage key prefix
   */
  this.storagePrefix = function (prefix) {
    if (!prefix) {
      return prefix;
    }
    $storagePrefix = prefix;
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useMissingTranslationHandlerLog
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells angular-translate to use built-in log handler when trying to translate
   * a translation Id which doesn't exist.
   *
   * This is actually a shortcut method for `useMissingTranslationHandler()`.
   *
   */
  this.useMissingTranslationHandlerLog = function () {
    return this.useMissingTranslationHandler('$translateMissingTranslationHandlerLog');
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useMissingTranslationHandler
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Expects a factory name which later gets instantiated with `$injector`.
   * This method can be used to tell angular-translate to use a custom
   * missingTranslationHandler. Just build a factory which returns a function
   * and expects a translation id as argument.
   *
   * Example:
   * <pre>
   *  app.config(function ($translateProvider) {
   *    $translateProvider.useMissingTranslationHandler('customHandler');
   *  });
   *
   *  app.factory('customHandler', function (dep1, dep2) {
   *    return function (translationId) {
   *      // something with translationId and dep1 and dep2
   *    };
   *  });
   * </pre>
   *
   * @param {string} factory Factory name
   */
  this.useMissingTranslationHandler = function (factory) {
    $missingTranslationHandlerFactory = factory;
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#usePostCompiling
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * If post compiling is enabled, all translated values will be processed
   * again with AngularJS' $compile.
   *
   * Example:
   * <pre>
   *  app.config(function ($translateProvider) {
   *    $translateProvider.usePostCompiling(true);
   *  });
   * </pre>
   *
   * @param {string} factory Factory name
   */
  this.usePostCompiling = function (value) {
    $postCompilingEnabled = !(!value);
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#forceAsyncReload
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * If force async reload is enabled, async loader will always be called
   * even if $translationTable already contains the language key, adding
   * possible new entries to the $translationTable.
   *
   * Example:
   * <pre>
   *  app.config(function ($translateProvider) {
   *    $translateProvider.forceAsyncReload(true);
   *  });
   * </pre>
   *
   * @param {boolean} value - valid values are true or false
   */
  this.forceAsyncReload = function (value) {
    $forceAsyncReloadEnabled = !(!value);
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#uniformLanguageTag
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells angular-translate which language tag should be used as a result when determining
   * the current browser language.
   *
   * This setting must be set before invoking {@link pascalprecht.translate.$translateProvider#methods_determinePreferredLanguage determinePreferredLanguage()}.
   *
   * <pre>
   * $translateProvider
   *   .uniformLanguageTag('bcp47')
   *   .determinePreferredLanguage()
   * </pre>
   *
   * The resolver currently supports:
   * * default
   *     (traditionally: hyphens will be converted into underscores, i.e. en-US => en_US)
   *     en-US => en_US
   *     en_US => en_US
   *     en-us => en_us
   * * java
   *     like default, but the second part will be always in uppercase
   *     en-US => en_US
   *     en_US => en_US
   *     en-us => en_US
   * * BCP 47 (RFC 4646 & 4647)
   *     en-US => en-US
   *     en_US => en-US
   *     en-us => en-US
   *
   * See also:
   * * http://en.wikipedia.org/wiki/IETF_language_tag
   * * http://www.w3.org/International/core/langtags/
   * * http://tools.ietf.org/html/bcp47
   *
   * @param {string|object} options - options (or standard)
   * @param {string} options.standard - valid values are 'default', 'bcp47', 'java'
   */
  this.uniformLanguageTag = function (options) {

    if (!options) {
      options = {};
    } else if (angular.isString(options)) {
      options = {
        standard: options
      };
    }

    uniformLanguageTagResolver = options.standard;

    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#determinePreferredLanguage
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Tells angular-translate to try to determine on its own which language key
   * to set as preferred language. When `fn` is given, angular-translate uses it
   * to determine a language key, otherwise it uses the built-in `getLocale()`
   * method.
   *
   * The `getLocale()` returns a language key in the format `[lang]_[country]` or
   * `[lang]` depending on what the browser provides.
   *
   * Use this method at your own risk, since not all browsers return a valid
   * locale (see {@link pascalprecht.translate.$translateProvider#methods_uniformLanguageTag uniformLanguageTag()}).
   *
   * @param {Function=} fn Function to determine a browser's locale
   */
  this.determinePreferredLanguage = function (fn) {

    var locale = (fn && angular.isFunction(fn)) ? fn() : getLocale();

    if (!$availableLanguageKeys.length) {
      $preferredLanguage = locale;
    } else {
      $preferredLanguage = negotiateLocale(locale) || locale;
    }

    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#registerAvailableLanguageKeys
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Registers a set of language keys the app will work with. Use this method in
   * combination with
   * {@link pascalprecht.translate.$translateProvider#determinePreferredLanguage determinePreferredLanguage}.
   * When available languages keys are registered, angular-translate
   * tries to find the best fitting language key depending on the browsers locale,
   * considering your language key convention.
   *
   * @param {object} languageKeys Array of language keys the your app will use
   * @param {object=} aliases Alias map.
   */
  this.registerAvailableLanguageKeys = function (languageKeys, aliases) {
    if (languageKeys) {
      $availableLanguageKeys = languageKeys;
      if (aliases) {
        $languageKeyAliases = aliases;
      }
      return this;
    }
    return $availableLanguageKeys;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#useLoaderCache
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Registers a cache for internal $http based loaders.
   * {@link pascalprecht.translate.$translationCache $translationCache}.
   * When false the cache will be disabled (default). When true or undefined
   * the cache will be a default (see $cacheFactory). When an object it will
   * be treat as a cache object itself: the usage is $http({cache: cache})
   *
   * @param {object} cache boolean, string or cache-object
   */
  this.useLoaderCache = function (cache) {
    if (cache === false) {
      // disable cache
      loaderCache = undefined;
    } else if (cache === true) {
      // enable cache using AJS defaults
      loaderCache = true;
    } else if (typeof(cache) === 'undefined') {
      // enable cache using default
      loaderCache = '$translationCache';
    } else if (cache) {
      // enable cache using given one (see $cacheFactory)
      loaderCache = cache;
    }
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#directivePriority
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Sets the default priority of the translate directive. The standard value is `0`.
   * Calling this function without an argument will return the current value.
   *
   * @param {number} priority for the translate-directive
   */
  this.directivePriority = function (priority) {
    if (priority === undefined) {
      // getter
      return directivePriority;
    } else {
      // setter with chaining
      directivePriority = priority;
      return this;
    }
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#statefulFilter
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * Since AngularJS 1.3, filters which are not stateless (depending at the scope)
   * have to explicit define this behavior.
   * Sets whether the translate filter should be stateful or stateless. The standard value is `true`
   * meaning being stateful.
   * Calling this function without an argument will return the current value.
   *
   * @param {boolean} state - defines the state of the filter
   */
  this.statefulFilter = function (state) {
    if (state === undefined) {
      // getter
      return statefulFilter;
    } else {
      // setter with chaining
      statefulFilter = state;
      return this;
    }
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#postProcess
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * The post processor will be intercept right after the translation result. It can modify the result.
   *
   * @param {object} fn Function or service name (string) to be called after the translation value has been set / resolved. The function itself will enrich every value being processed and then continue the normal resolver process
   */
  this.postProcess = function (fn) {
    if (fn) {
      postProcessFn = fn;
    } else {
      postProcessFn = undefined;
    }
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateProvider#keepContent
   * @methodOf pascalprecht.translate.$translateProvider
   *
   * @description
   * If keepContent is set to true than translate directive will always use innerHTML
   * as a default translation
   *
   * Example:
   * <pre>
   *  app.config(function ($translateProvider) {
   *    $translateProvider.keepContent(true);
   *  });
   * </pre>
   *
   * @param {boolean} value - valid values are true or false
   */
  this.keepContent = function (value) {
    $keepContent = !(!value);
    return this;
  };

  /**
   * @ngdoc object
   * @name pascalprecht.translate.$translate
   * @requires $interpolate
   * @requires $log
   * @requires $rootScope
   * @requires $q
   *
   * @description
   * The `$translate` service is the actual core of angular-translate. It expects a translation id
   * and optional interpolate parameters to translate contents.
   *
   * <pre>
   *  $translate('HEADLINE_TEXT').then(function (translation) {
   *    $scope.translatedText = translation;
   *  });
   * </pre>
   *
   * @param {string|array} translationId A token which represents a translation id
   *                                     This can be optionally an array of translation ids which
   *                                     results that the function returns an object where each key
   *                                     is the translation id and the value the translation.
   * @param {object=} interpolateParams An object hash for dynamic values
   * @param {string} interpolationId The id of the interpolation to use
   * @param {string} defaultTranslationText the optional default translation text that is written as
   *                                        as default text in case it is not found in any configured language
   * @param {string} forceLanguage A language to be used instead of the current language
   * @returns {object} promise
   */
  this.$get = [
    '$log',
    '$injector',
    '$rootScope',
    '$q',
    function ($log, $injector, $rootScope, $q) {

      var Storage,
          defaultInterpolator = $injector.get($interpolationFactory || '$translateDefaultInterpolation'),
          pendingLoader = false,
          interpolatorHashMap = {},
          langPromises = {},
          fallbackIndex,
          startFallbackIteration;

      var $translate = function (translationId, interpolateParams, interpolationId, defaultTranslationText, forceLanguage) {
        if (!$uses && $preferredLanguage) {
          $uses = $preferredLanguage;
        }
        var uses = (forceLanguage && forceLanguage !== $uses) ? // we don't want to re-negotiate $uses
              (negotiateLocale(forceLanguage) || forceLanguage) : $uses;

        // Check forceLanguage is present
        if (forceLanguage) {
          loadTranslationsIfMissing(forceLanguage);
        }

        // Duck detection: If the first argument is an array, a bunch of translations was requested.
        // The result is an object.
        if (angular.isArray(translationId)) {
          // Inspired by Q.allSettled by Kris Kowal
          // https://github.com/kriskowal/q/blob/b0fa72980717dc202ffc3cbf03b936e10ebbb9d7/q.js#L1553-1563
          // This transforms all promises regardless resolved or rejected
          var translateAll = function (translationIds) {
            var results = {}; // storing the actual results
            var promises = []; // promises to wait for
            // Wraps the promise a) being always resolved and b) storing the link id->value
            var translate = function (translationId) {
              var deferred = $q.defer();
              var regardless = function (value) {
                results[translationId] = value;
                deferred.resolve([translationId, value]);
              };
              // we don't care whether the promise was resolved or rejected; just store the values
              $translate(translationId, interpolateParams, interpolationId, defaultTranslationText, forceLanguage).then(regardless, regardless);
              return deferred.promise;
            };
            for (var i = 0, c = translationIds.length; i < c; i++) {
              promises.push(translate(translationIds[i]));
            }
            // wait for all (including storing to results)
            return $q.all(promises).then(function () {
              // return the results
              return results;
            });
          };
          return translateAll(translationId);
        }

        var deferred = $q.defer();

        // trim off any whitespace
        if (translationId) {
          translationId = trim.apply(translationId);
        }

        var promiseToWaitFor = (function () {
          var promise = $preferredLanguage ?
            langPromises[$preferredLanguage] :
            langPromises[uses];

          fallbackIndex = 0;

          if ($storageFactory && !promise) {
            // looks like there's no pending promise for $preferredLanguage or
            // $uses. Maybe there's one pending for a language that comes from
            // storage.
            var langKey = Storage.get($storageKey);
            promise = langPromises[langKey];

            if ($fallbackLanguage && $fallbackLanguage.length) {
                var index = indexOf($fallbackLanguage, langKey);
                // maybe the language from storage is also defined as fallback language
                // we increase the fallback language index to not search in that language
                // as fallback, since it's probably the first used language
                // in that case the index starts after the first element
                fallbackIndex = (index === 0) ? 1 : 0;

                // but we can make sure to ALWAYS fallback to preferred language at least
                if (indexOf($fallbackLanguage, $preferredLanguage) < 0) {
                  $fallbackLanguage.push($preferredLanguage);
                }
            }
          }
          return promise;
        }());

        if (!promiseToWaitFor) {
          // no promise to wait for? okay. Then there's no loader registered
          // nor is a one pending for language that comes from storage.
          // We can just translate.
          determineTranslation(translationId, interpolateParams, interpolationId, defaultTranslationText, uses).then(deferred.resolve, deferred.reject);
        } else {
          var promiseResolved = function () {
            // $uses may have changed while waiting
            if (!forceLanguage) {
              uses = $uses;
            }
            determineTranslation(translationId, interpolateParams, interpolationId, defaultTranslationText, uses).then(deferred.resolve, deferred.reject);
          };
          promiseResolved.displayName = 'promiseResolved';

          promiseToWaitFor['finally'](promiseResolved);
        }
        return deferred.promise;
      };

      /**
       * @name applyNotFoundIndicators
       * @private
       *
       * @description
       * Applies not fount indicators to given translation id, if needed.
       * This function gets only executed, if a translation id doesn't exist,
       * which is why a translation id is expected as argument.
       *
       * @param {string} translationId Translation id.
       * @returns {string} Same as given translation id but applied with not found
       * indicators.
       */
      var applyNotFoundIndicators = function (translationId) {
        // applying notFoundIndicators
        if ($notFoundIndicatorLeft) {
          translationId = [$notFoundIndicatorLeft, translationId].join(' ');
        }
        if ($notFoundIndicatorRight) {
          translationId = [translationId, $notFoundIndicatorRight].join(' ');
        }
        return translationId;
      };

      /**
       * @name useLanguage
       * @private
       *
       * @description
       * Makes actual use of a language by setting a given language key as used
       * language and informs registered interpolators to also use the given
       * key as locale.
       *
       * @param {string} key Locale key.
       */
      var useLanguage = function (key) {
        $uses = key;

        // make sure to store new language key before triggering success event
        if ($storageFactory) {
          Storage.put($translate.storageKey(), $uses);
        }

        $rootScope.$emit('$translateChangeSuccess', {language: key});

        // inform default interpolator
        defaultInterpolator.setLocale($uses);

        var eachInterpolator = function (interpolator, id) {
          interpolatorHashMap[id].setLocale($uses);
        };
        eachInterpolator.displayName = 'eachInterpolatorLocaleSetter';

        // inform all others too!
        angular.forEach(interpolatorHashMap, eachInterpolator);
        $rootScope.$emit('$translateChangeEnd', {language: key});
      };

      /**
       * @name loadAsync
       * @private
       *
       * @description
       * Kicks of registered async loader using `$injector` and applies existing
       * loader options. When resolved, it updates translation tables accordingly
       * or rejects with given language key.
       *
       * @param {string} key Language key.
       * @return {Promise} A promise.
       */
      var loadAsync = function (key) {
        if (!key) {
          throw 'No language key specified for loading.';
        }

        var deferred = $q.defer();

        $rootScope.$emit('$translateLoadingStart', {language: key});
        pendingLoader = true;

        var cache = loaderCache;
        if (typeof(cache) === 'string') {
          // getting on-demand instance of loader
          cache = $injector.get(cache);
        }

        var loaderOptions = angular.extend({}, $loaderOptions, {
          key: key,
          $http: angular.extend({}, {
            cache: cache
          }, $loaderOptions.$http)
        });

        var onLoaderSuccess = function (data) {
          var translationTable = {};
          $rootScope.$emit('$translateLoadingSuccess', {language: key});

          if (angular.isArray(data)) {
            angular.forEach(data, function (table) {
              angular.extend(translationTable, flatObject(table));
            });
          } else {
            angular.extend(translationTable, flatObject(data));
          }
          pendingLoader = false;
          deferred.resolve({
            key: key,
            table: translationTable
          });
          $rootScope.$emit('$translateLoadingEnd', {language: key});
        };
        onLoaderSuccess.displayName = 'onLoaderSuccess';

        var onLoaderError = function (key) {
          $rootScope.$emit('$translateLoadingError', {language: key});
          deferred.reject(key);
          $rootScope.$emit('$translateLoadingEnd', {language: key});
        };
        onLoaderError.displayName = 'onLoaderError';

        $injector.get($loaderFactory)(loaderOptions)
          .then(onLoaderSuccess, onLoaderError);

        return deferred.promise;
      };

      if ($storageFactory) {
        Storage = $injector.get($storageFactory);

        if (!Storage.get || !Storage.put) {
          throw new Error('Couldn\'t use storage \'' + $storageFactory + '\', missing get() or put() method!');
        }
      }

      // if we have additional interpolations that were added via
      // $translateProvider.addInterpolation(), we have to map'em
      if ($interpolatorFactories.length) {
        var eachInterpolationFactory = function (interpolatorFactory) {
          var interpolator = $injector.get(interpolatorFactory);
          // setting initial locale for each interpolation service
          interpolator.setLocale($preferredLanguage || $uses);
          // make'em recognizable through id
          interpolatorHashMap[interpolator.getInterpolationIdentifier()] = interpolator;
        };
        eachInterpolationFactory.displayName = 'interpolationFactoryAdder';

        angular.forEach($interpolatorFactories, eachInterpolationFactory);
      }

      /**
       * @name getTranslationTable
       * @private
       *
       * @description
       * Returns a promise that resolves to the translation table
       * or is rejected if an error occurred.
       *
       * @param langKey
       * @returns {Q.promise}
       */
      var getTranslationTable = function (langKey) {
        var deferred = $q.defer();
        if (Object.prototype.hasOwnProperty.call($translationTable, langKey)) {
          deferred.resolve($translationTable[langKey]);
        } else if (langPromises[langKey]) {
          var onResolve = function (data) {
            translations(data.key, data.table);
            deferred.resolve(data.table);
          };
          onResolve.displayName = 'translationTableResolver';
          langPromises[langKey].then(onResolve, deferred.reject);
        } else {
          deferred.reject();
        }
        return deferred.promise;
      };

      /**
       * @name getFallbackTranslation
       * @private
       *
       * @description
       * Returns a promise that will resolve to the translation
       * or be rejected if no translation was found for the language.
       * This function is currently only used for fallback language translation.
       *
       * @param langKey The language to translate to.
       * @param translationId
       * @param interpolateParams
       * @param Interpolator
       * @returns {Q.promise}
       */
      var getFallbackTranslation = function (langKey, translationId, interpolateParams, Interpolator) {
        var deferred = $q.defer();

        var onResolve = function (translationTable) {
          if (Object.prototype.hasOwnProperty.call(translationTable, translationId)) {
            Interpolator.setLocale(langKey);
            var translation = translationTable[translationId];
            if (translation.substr(0, 2) === '@:') {
              getFallbackTranslation(langKey, translation.substr(2), interpolateParams, Interpolator)
                .then(deferred.resolve, deferred.reject);
            } else {
              var interpolatedValue = Interpolator.interpolate(translationTable[translationId], interpolateParams);
              interpolatedValue = applyPostProcessing(translationId, translationTable[translationId], interpolatedValue, interpolateParams, langKey);

              deferred.resolve(interpolatedValue);

            }
            Interpolator.setLocale($uses);
          } else {
            deferred.reject();
          }
        };
        onResolve.displayName = 'fallbackTranslationResolver';

        getTranslationTable(langKey).then(onResolve, deferred.reject);

        return deferred.promise;
      };

      /**
       * @name getFallbackTranslationInstant
       * @private
       *
       * @description
       * Returns a translation
       * This function is currently only used for fallback language translation.
       *
       * @param langKey The language to translate to.
       * @param translationId
       * @param interpolateParams
       * @param Interpolator
       * @returns {string} translation
       */
      var getFallbackTranslationInstant = function (langKey, translationId, interpolateParams, Interpolator) {
        var result, translationTable = $translationTable[langKey];

        if (translationTable && Object.prototype.hasOwnProperty.call(translationTable, translationId)) {
          Interpolator.setLocale(langKey);
          result = Interpolator.interpolate(translationTable[translationId], interpolateParams);
          result = applyPostProcessing(translationId, translationTable[translationId], result, interpolateParams, langKey);
          if (result.substr(0, 2) === '@:') {
            return getFallbackTranslationInstant(langKey, result.substr(2), interpolateParams, Interpolator);
          }
          Interpolator.setLocale($uses);
        }

        return result;
      };


      /**
       * @name translateByHandler
       * @private
       *
       * Translate by missing translation handler.
       *
       * @param translationId
       * @param interpolateParams
       * @param defaultTranslationText
       * @returns translation created by $missingTranslationHandler or translationId is $missingTranslationHandler is
       * absent
       */
      var translateByHandler = function (translationId, interpolateParams, defaultTranslationText) {
        // If we have a handler factory - we might also call it here to determine if it provides
        // a default text for a translationid that can't be found anywhere in our tables
        if ($missingTranslationHandlerFactory) {
          var resultString = $injector.get($missingTranslationHandlerFactory)(translationId, $uses, interpolateParams, defaultTranslationText);
          if (resultString !== undefined) {
            return resultString;
          } else {
            return translationId;
          }
        } else {
          return translationId;
        }
      };

      /**
       * @name resolveForFallbackLanguage
       * @private
       *
       * Recursive helper function for fallbackTranslation that will sequentially look
       * for a translation in the fallbackLanguages starting with fallbackLanguageIndex.
       *
       * @param fallbackLanguageIndex
       * @param translationId
       * @param interpolateParams
       * @param Interpolator
       * @returns {Q.promise} Promise that will resolve to the translation.
       */
      var resolveForFallbackLanguage = function (fallbackLanguageIndex, translationId, interpolateParams, Interpolator, defaultTranslationText) {
        var deferred = $q.defer();

        if (fallbackLanguageIndex < $fallbackLanguage.length) {
          var langKey = $fallbackLanguage[fallbackLanguageIndex];
          getFallbackTranslation(langKey, translationId, interpolateParams, Interpolator).then(
            function (data) {
                deferred.resolve(data);
            },
            function () {
              // Look in the next fallback language for a translation.
              // It delays the resolving by passing another promise to resolve.
              return resolveForFallbackLanguage(fallbackLanguageIndex + 1, translationId, interpolateParams, Interpolator, defaultTranslationText).then(deferred.resolve, deferred.reject);
            }
          );
        } else {
          // No translation found in any fallback language
          // if a default translation text is set in the directive, then return this as a result
          if (defaultTranslationText) {
            deferred.resolve(defaultTranslationText);
          } else {
            // if no default translation is set and an error handler is defined, send it to the handler
            // and then return the result
            if ($missingTranslationHandlerFactory) {
              deferred.resolve(translateByHandler(translationId, interpolateParams));
            } else {
              deferred.reject(translateByHandler(translationId, interpolateParams));
            }

          }
        }
        return deferred.promise;
      };

      /**
       * @name resolveForFallbackLanguageInstant
       * @private
       *
       * Recursive helper function for fallbackTranslation that will sequentially look
       * for a translation in the fallbackLanguages starting with fallbackLanguageIndex.
       *
       * @param fallbackLanguageIndex
       * @param translationId
       * @param interpolateParams
       * @param Interpolator
       * @returns {string} translation
       */
      var resolveForFallbackLanguageInstant = function (fallbackLanguageIndex, translationId, interpolateParams, Interpolator) {
        var result;

        if (fallbackLanguageIndex < $fallbackLanguage.length) {
          var langKey = $fallbackLanguage[fallbackLanguageIndex];
          result = getFallbackTranslationInstant(langKey, translationId, interpolateParams, Interpolator);
          if (!result) {
            result = resolveForFallbackLanguageInstant(fallbackLanguageIndex + 1, translationId, interpolateParams, Interpolator);
          }
        }
        return result;
      };

      /**
       * Translates with the usage of the fallback languages.
       *
       * @param translationId
       * @param interpolateParams
       * @param Interpolator
       * @returns {Q.promise} Promise, that resolves to the translation.
       */
      var fallbackTranslation = function (translationId, interpolateParams, Interpolator, defaultTranslationText) {
        // Start with the fallbackLanguage with index 0
        return resolveForFallbackLanguage((startFallbackIteration>0 ? startFallbackIteration : fallbackIndex), translationId, interpolateParams, Interpolator, defaultTranslationText);
      };

      /**
       * Translates with the usage of the fallback languages.
       *
       * @param translationId
       * @param interpolateParams
       * @param Interpolator
       * @returns {String} translation
       */
      var fallbackTranslationInstant = function (translationId, interpolateParams, Interpolator) {
        // Start with the fallbackLanguage with index 0
        return resolveForFallbackLanguageInstant((startFallbackIteration>0 ? startFallbackIteration : fallbackIndex), translationId, interpolateParams, Interpolator);
      };

      var determineTranslation = function (translationId, interpolateParams, interpolationId, defaultTranslationText, uses) {

        var deferred = $q.defer();

        var table = uses ? $translationTable[uses] : $translationTable,
            Interpolator = (interpolationId) ? interpolatorHashMap[interpolationId] : defaultInterpolator;

        // if the translation id exists, we can just interpolate it
        if (table && Object.prototype.hasOwnProperty.call(table, translationId)) {
          var translation = table[translationId];

          // If using link, rerun $translate with linked translationId and return it
          if (translation.substr(0, 2) === '@:') {

            $translate(translation.substr(2), interpolateParams, interpolationId, defaultTranslationText, uses)
              .then(deferred.resolve, deferred.reject);
          } else {
            //
            var resolvedTranslation = Interpolator.interpolate(translation, interpolateParams);
            resolvedTranslation = applyPostProcessing(translationId, translation, resolvedTranslation, interpolateParams, uses);
            deferred.resolve(resolvedTranslation);
          }
        } else {
          var missingTranslationHandlerTranslation;
          // for logging purposes only (as in $translateMissingTranslationHandlerLog), value is not returned to promise
          if ($missingTranslationHandlerFactory && !pendingLoader) {
            missingTranslationHandlerTranslation = translateByHandler(translationId, interpolateParams, defaultTranslationText);
          }

          // since we couldn't translate the inital requested translation id,
          // we try it now with one or more fallback languages, if fallback language(s) is
          // configured.
          if (uses && $fallbackLanguage && $fallbackLanguage.length) {
            fallbackTranslation(translationId, interpolateParams, Interpolator, defaultTranslationText)
                .then(function (translation) {
                  deferred.resolve(translation);
                }, function (_translationId) {
                  deferred.reject(applyNotFoundIndicators(_translationId));
                });
          } else if ($missingTranslationHandlerFactory && !pendingLoader && missingTranslationHandlerTranslation) {
            // looks like the requested translation id doesn't exists.
            // Now, if there is a registered handler for missing translations and no
            // asyncLoader is pending, we execute the handler
            if (defaultTranslationText) {
              deferred.resolve(defaultTranslationText);
              } else {
                deferred.resolve(missingTranslationHandlerTranslation);
              }
          } else {
            if (defaultTranslationText) {
              deferred.resolve(defaultTranslationText);
            } else {
              deferred.reject(applyNotFoundIndicators(translationId));
            }
          }
        }
        return deferred.promise;
      };

      var determineTranslationInstant = function (translationId, interpolateParams, interpolationId, uses) {

        var result, table = uses ? $translationTable[uses] : $translationTable,
            Interpolator = defaultInterpolator;

        // if the interpolation id exists use custom interpolator
        if (interpolatorHashMap && Object.prototype.hasOwnProperty.call(interpolatorHashMap, interpolationId)) {
          Interpolator = interpolatorHashMap[interpolationId];
        }

        // if the translation id exists, we can just interpolate it
        if (table && Object.prototype.hasOwnProperty.call(table, translationId)) {
          var translation = table[translationId];

          // If using link, rerun $translate with linked translationId and return it
          if (translation.substr(0, 2) === '@:') {
            result = determineTranslationInstant(translation.substr(2), interpolateParams, interpolationId, uses);
          } else {
            result = Interpolator.interpolate(translation, interpolateParams);
            result = applyPostProcessing(translationId, translation, result, interpolateParams, uses);
          }
        } else {
          var missingTranslationHandlerTranslation;
          // for logging purposes only (as in $translateMissingTranslationHandlerLog), value is not returned to promise
          if ($missingTranslationHandlerFactory && !pendingLoader) {
            missingTranslationHandlerTranslation = translateByHandler(translationId, interpolateParams);
          }

          // since we couldn't translate the inital requested translation id,
          // we try it now with one or more fallback languages, if fallback language(s) is
          // configured.
          if (uses && $fallbackLanguage && $fallbackLanguage.length) {
            fallbackIndex = 0;
            result = fallbackTranslationInstant(translationId, interpolateParams, Interpolator);
          } else if ($missingTranslationHandlerFactory && !pendingLoader && missingTranslationHandlerTranslation) {
            // looks like the requested translation id doesn't exists.
            // Now, if there is a registered handler for missing translations and no
            // asyncLoader is pending, we execute the handler
            result = missingTranslationHandlerTranslation;
          } else {
            result = applyNotFoundIndicators(translationId);
          }
        }

        return result;
      };

      var clearNextLangAndPromise = function(key) {
        if ($nextLang === key) {
          $nextLang = undefined;
        }
        langPromises[key] = undefined;
      };

      var applyPostProcessing = function (translationId, translation, resolvedTranslation, interpolateParams, uses) {
        var fn = postProcessFn;

        if (fn) {

          if (typeof(fn) === 'string') {
            // getting on-demand instance
            fn = $injector.get(fn);
          }
          if (fn) {
            return fn(translationId, translation, resolvedTranslation, interpolateParams, uses);
          }
        }

        return resolvedTranslation;
      };

      var loadTranslationsIfMissing = function (key) {
        if (!$translationTable[key] && $loaderFactory && !langPromises[key]) {
          langPromises[key] = loadAsync(key).then(function (translation) {
            translations(translation.key, translation.table);
            return translation;
          });
        }
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#preferredLanguage
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns the language key for the preferred language.
       *
       * @param {string} langKey language String or Array to be used as preferredLanguage (changing at runtime)
       *
       * @return {string} preferred language key
       */
      $translate.preferredLanguage = function (langKey) {
        if(langKey) {
          setupPreferredLanguage(langKey);
        }
        return $preferredLanguage;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#cloakClassName
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns the configured class name for `translate-cloak` directive.
       *
       * @return {string} cloakClassName
       */
      $translate.cloakClassName = function () {
        return $cloakClassName;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#nestedObjectDelimeter
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns the configured delimiter for nested namespaces.
       *
       * @return {string} nestedObjectDelimeter
       */
      $translate.nestedObjectDelimeter = function () {
        return $nestedObjectDelimeter;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#fallbackLanguage
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns the language key for the fallback languages or sets a new fallback stack.
       *
       * @param {string=} langKey language String or Array of fallback languages to be used (to change stack at runtime)
       *
       * @return {string||array} fallback language key
       */
      $translate.fallbackLanguage = function (langKey) {
        if (langKey !== undefined && langKey !== null) {
          fallbackStack(langKey);

          // as we might have an async loader initiated and a new translation language might have been defined
          // we need to add the promise to the stack also. So - iterate.
          if ($loaderFactory) {
            if ($fallbackLanguage && $fallbackLanguage.length) {
              for (var i = 0, len = $fallbackLanguage.length; i < len; i++) {
                if (!langPromises[$fallbackLanguage[i]]) {
                  langPromises[$fallbackLanguage[i]] = loadAsync($fallbackLanguage[i]);
                }
              }
            }
          }
          $translate.use($translate.use());
        }
        if ($fallbackWasString) {
          return $fallbackLanguage[0];
        } else {
          return $fallbackLanguage;
        }

      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#useFallbackLanguage
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Sets the first key of the fallback language stack to be used for translation.
       * Therefore all languages in the fallback array BEFORE this key will be skipped!
       *
       * @param {string=} langKey Contains the langKey the iteration shall start with. Set to false if you want to
       * get back to the whole stack
       */
      $translate.useFallbackLanguage = function (langKey) {
        if (langKey !== undefined && langKey !== null) {
          if (!langKey) {
            startFallbackIteration = 0;
          } else {
            var langKeyPosition = indexOf($fallbackLanguage, langKey);
            if (langKeyPosition > -1) {
              startFallbackIteration = langKeyPosition;
            }
          }

        }

      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#proposedLanguage
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns the language key of language that is currently loaded asynchronously.
       *
       * @return {string} language key
       */
      $translate.proposedLanguage = function () {
        return $nextLang;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#storage
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns registered storage.
       *
       * @return {object} Storage
       */
      $translate.storage = function () {
        return Storage;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#negotiateLocale
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns a language key based on available languages and language aliases. If a
       * language key cannot be resolved, returns undefined.
       *
       * If no or a falsy key is given, returns undefined.
       *
       * @param {string} [key] Language key
       * @return {string|undefined} Language key or undefined if no language key is found.
       */
      $translate.negotiateLocale = negotiateLocale;

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#use
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Tells angular-translate which language to use by given language key. This method is
       * used to change language at runtime. It also takes care of storing the language
       * key in a configured store to let your app remember the choosed language.
       *
       * When trying to 'use' a language which isn't available it tries to load it
       * asynchronously with registered loaders.
       *
       * Returns promise object with loaded language file data or string of the currently used language.
       *
       * If no or a falsy key is given it returns the currently used language key.
       * The returned string will be ```undefined``` if setting up $translate hasn't finished.
       * @example
       * $translate.use("en_US").then(function(data){
       *   $scope.text = $translate("HELLO");
       * });
       *
       * @param {string} [key] Language key
       * @return {object|string} Promise with loaded language data or the language key if a falsy param was given.
       */
      $translate.use = function (key) {
        if (!key) {
          return $uses;
        }

        var deferred = $q.defer();

        $rootScope.$emit('$translateChangeStart', {language: key});

        // Try to get the aliased language key
        var aliasedKey = negotiateLocale(key);
        // Ensure only registered language keys will be loaded
        if ($availableLanguageKeys.length > 0 && !aliasedKey) {
          return $q.reject(key);
        }

        if (aliasedKey) {
          key = aliasedKey;
        }

        // if there isn't a translation table for the language we've requested,
        // we load it asynchronously
        $nextLang = key;
        if (($forceAsyncReloadEnabled || !$translationTable[key]) && $loaderFactory && !langPromises[key]) {
          langPromises[key] = loadAsync(key).then(function (translation) {
            translations(translation.key, translation.table);
            deferred.resolve(translation.key);
            if ($nextLang === key) {
              useLanguage(translation.key);
            }
            return translation;
          }, function (key) {
            $rootScope.$emit('$translateChangeError', {language: key});
            deferred.reject(key);
            $rootScope.$emit('$translateChangeEnd', {language: key});
            return $q.reject(key);
          });
          langPromises[key]['finally'](function () {
            clearNextLangAndPromise(key);
          });
        } else if (langPromises[key]) {
          // we are already loading this asynchronously
          // resolve our new deferred when the old langPromise is resolved
          langPromises[key].then(function (translation) {
            if ($nextLang === translation.key) {
              useLanguage(translation.key);
            }
            deferred.resolve(translation.key);
            return translation;
          }, function (key) {
            // find first available fallback language if that request has failed
            if (!$uses && $fallbackLanguage && $fallbackLanguage.length > 0) {
              return $translate.use($fallbackLanguage[0]).then(deferred.resolve, deferred.reject);
            } else {
              return deferred.reject(key);
            }
          });
        } else {
          deferred.resolve(key);
          useLanguage(key);
        }

        return deferred.promise;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#resolveClientLocale
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * This returns the current browser/client's language key. The result is processed with the configured uniform tag resolver.
       *
       * @returns {string} the current client/browser language key
       */
      $translate.resolveClientLocale = function () {
        return getLocale();
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#storageKey
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns the key for the storage.
       *
       * @return {string} storage key
       */
      $translate.storageKey = function () {
        return storageKey();
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#isPostCompilingEnabled
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns whether post compiling is enabled or not
       *
       * @return {bool} storage key
       */
      $translate.isPostCompilingEnabled = function () {
        return $postCompilingEnabled;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#isForceAsyncReloadEnabled
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns whether force async reload is enabled or not
       *
       * @return {boolean} forceAsyncReload value
       */
      $translate.isForceAsyncReloadEnabled = function () {
        return $forceAsyncReloadEnabled;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#isKeepContent
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns whether keepContent or not
       *
       * @return {boolean} keepContent value
       */
      $translate.isKeepContent = function () {
        return $keepContent;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#refresh
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Refreshes a translation table pointed by the given langKey. If langKey is not specified,
       * the module will drop all existent translation tables and load new version of those which
       * are currently in use.
       *
       * Refresh means that the module will drop target translation table and try to load it again.
       *
       * In case there are no loaders registered the refresh() method will throw an Error.
       *
       * If the module is able to refresh translation tables refresh() method will broadcast
       * $translateRefreshStart and $translateRefreshEnd events.
       *
       * @example
       * // this will drop all currently existent translation tables and reload those which are
       * // currently in use
       * $translate.refresh();
       * // this will refresh a translation table for the en_US language
       * $translate.refresh('en_US');
       *
       * @param {string} langKey A language key of the table, which has to be refreshed
       *
       * @return {promise} Promise, which will be resolved in case a translation tables refreshing
       * process is finished successfully, and reject if not.
       */
      $translate.refresh = function (langKey) {
        if (!$loaderFactory) {
          throw new Error('Couldn\'t refresh translation table, no loader registered!');
        }

        var deferred = $q.defer();

        function resolve() {
          deferred.resolve();
          $rootScope.$emit('$translateRefreshEnd', {language: langKey});
        }

        function reject() {
          deferred.reject();
          $rootScope.$emit('$translateRefreshEnd', {language: langKey});
        }

        $rootScope.$emit('$translateRefreshStart', {language: langKey});

        if (!langKey) {
          // if there's no language key specified we refresh ALL THE THINGS!
          var tables = [], loadingKeys = {};

          // reload registered fallback languages
          if ($fallbackLanguage && $fallbackLanguage.length) {
            for (var i = 0, len = $fallbackLanguage.length; i < len; i++) {
              tables.push(loadAsync($fallbackLanguage[i]));
              loadingKeys[$fallbackLanguage[i]] = true;
            }
          }

          // reload currently used language
          if ($uses && !loadingKeys[$uses]) {
            tables.push(loadAsync($uses));
          }

          var allTranslationsLoaded = function (tableData) {
            $translationTable = {};
            angular.forEach(tableData, function (data) {
              translations(data.key, data.table);
            });
            if ($uses) {
              useLanguage($uses);
            }
            resolve();
          };
          allTranslationsLoaded.displayName = 'refreshPostProcessor';

          $q.all(tables).then(allTranslationsLoaded, reject);

        } else if ($translationTable[langKey]) {

          var oneTranslationsLoaded = function (data) {
            translations(data.key, data.table);
            if (langKey === $uses) {
              useLanguage($uses);
            }
            resolve();
            return data;
          };
          oneTranslationsLoaded.displayName = 'refreshPostProcessor';

          loadAsync(langKey).then(oneTranslationsLoaded, reject);

        } else {
          reject();
        }
        return deferred.promise;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#instant
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns a translation instantly from the internal state of loaded translation. All rules
       * regarding the current language, the preferred language of even fallback languages will be
       * used except any promise handling. If a language was not found, an asynchronous loading
       * will be invoked in the background.
       *
       * @param {string|array} translationId A token which represents a translation id
       *                                     This can be optionally an array of translation ids which
       *                                     results that the function's promise returns an object where
       *                                     each key is the translation id and the value the translation.
       * @param {object} interpolateParams Params
       * @param {string} interpolationId The id of the interpolation to use
       * @param {string} forceLanguage A language to be used instead of the current language
       *
       * @return {string|object} translation
       */
      $translate.instant = function (translationId, interpolateParams, interpolationId, forceLanguage) {

        // we don't want to re-negotiate $uses
        var uses = (forceLanguage && forceLanguage !== $uses) ? // we don't want to re-negotiate $uses
              (negotiateLocale(forceLanguage) || forceLanguage) : $uses;

        // Detect undefined and null values to shorten the execution and prevent exceptions
        if (translationId === null || angular.isUndefined(translationId)) {
          return translationId;
        }

        // Check forceLanguage is present
        if (forceLanguage) {
          loadTranslationsIfMissing(forceLanguage);
        }

        // Duck detection: If the first argument is an array, a bunch of translations was requested.
        // The result is an object.
        if (angular.isArray(translationId)) {
          var results = {};
          for (var i = 0, c = translationId.length; i < c; i++) {
            results[translationId[i]] = $translate.instant(translationId[i], interpolateParams, interpolationId, forceLanguage);
          }
          return results;
        }

        // We discarded unacceptable values. So we just need to verify if translationId is empty String
        if (angular.isString(translationId) && translationId.length < 1) {
          return translationId;
        }

        // trim off any whitespace
        if (translationId) {
          translationId = trim.apply(translationId);
        }

        var result, possibleLangKeys = [];
        if ($preferredLanguage) {
          possibleLangKeys.push($preferredLanguage);
        }
        if (uses) {
          possibleLangKeys.push(uses);
        }
        if ($fallbackLanguage && $fallbackLanguage.length) {
          possibleLangKeys = possibleLangKeys.concat($fallbackLanguage);
        }
        for (var j = 0, d = possibleLangKeys.length; j < d; j++) {
          var possibleLangKey = possibleLangKeys[j];
          if ($translationTable[possibleLangKey]) {
            if (typeof $translationTable[possibleLangKey][translationId] !== 'undefined') {
              result = determineTranslationInstant(translationId, interpolateParams, interpolationId, uses);
            }
          }
          if (typeof result !== 'undefined') {
            break;
          }
        }

        if (!result && result !== '') {
          if ($notFoundIndicatorLeft || $notFoundIndicatorRight) {
            result = applyNotFoundIndicators(translationId);
          } else {
            // Return translation of default interpolator if not found anything.
            result = defaultInterpolator.interpolate(translationId, interpolateParams);
            if ($missingTranslationHandlerFactory && !pendingLoader) {
              result = translateByHandler(translationId, interpolateParams);
            }
          }
        }

        return result;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#versionInfo
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns the current version information for the angular-translate library
       *
       * @return {string} angular-translate version
       */
      $translate.versionInfo = function () {
        return version;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#loaderCache
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns the defined loaderCache.
       *
       * @return {boolean|string|object} current value of loaderCache
       */
      $translate.loaderCache = function () {
        return loaderCache;
      };

      // internal purpose only
      $translate.directivePriority = function () {
        return directivePriority;
      };

      // internal purpose only
      $translate.statefulFilter = function () {
        return statefulFilter;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#isReady
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns whether the service is "ready" to translate (i.e. loading 1st language).
       *
       * See also {@link pascalprecht.translate.$translate#methods_onReady onReady()}.
       *
       * @return {boolean} current value of ready
       */
      $translate.isReady = function () {
        return $isReady;
      };

      var $onReadyDeferred = $q.defer();
      $onReadyDeferred.promise.then(function () {
        $isReady = true;
      });

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#onReady
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * Returns whether the service is "ready" to translate (i.e. loading 1st language).
       *
       * See also {@link pascalprecht.translate.$translate#methods_isReady isReady()}.
       *
       * @param {Function=} fn Function to invoke when service is ready
       * @return {object} Promise resolved when service is ready
       */
      $translate.onReady = function (fn) {
        var deferred = $q.defer();
        if (angular.isFunction(fn)) {
          deferred.promise.then(fn);
        }
        if ($isReady) {
          deferred.resolve();
        } else {
          $onReadyDeferred.promise.then(deferred.resolve);
        }
        return deferred.promise;
      };

      /**
       * @ngdoc function
       * @name pascalprecht.translate.$translate#getAvailableLanguageKeys
       * @methodOf pascalprecht.translate.$translate
       *
       * @description
       * This function simply returns the registered language keys being defined before in the config phase
       * With this, an application can use the array to provide a language selection dropdown or similar
       * without any additional effort
       *
       * @returns {object} returns the list of possibly registered language keys and mapping or null if not defined
       */
      $translate.getAvailableLanguageKeys = function () {
        if ($availableLanguageKeys.length > 0) {
          return $availableLanguageKeys;
        }
        return null;
      };

      // Whenever $translateReady is being fired, this will ensure the state of $isReady
      var globalOnReadyListener = $rootScope.$on('$translateReady', function () {
        $onReadyDeferred.resolve();
        globalOnReadyListener(); // one time only
        globalOnReadyListener = null;
      });
      var globalOnChangeListener = $rootScope.$on('$translateChangeEnd', function () {
        $onReadyDeferred.resolve();
        globalOnChangeListener(); // one time only
        globalOnChangeListener = null;
      });

      if ($loaderFactory) {

        // If at least one async loader is defined and there are no
        // (default) translations available we should try to load them.
        if (angular.equals($translationTable, {})) {
          if ($translate.use()) {
            $translate.use($translate.use());
          }
        }

        // Also, if there are any fallback language registered, we start
        // loading them asynchronously as soon as we can.
        if ($fallbackLanguage && $fallbackLanguage.length) {
          var processAsyncResult = function (translation) {
            translations(translation.key, translation.table);
            $rootScope.$emit('$translateChangeEnd', { language: translation.key });
            return translation;
          };
          for (var i = 0, len = $fallbackLanguage.length; i < len; i++) {
            var fallbackLanguageId = $fallbackLanguage[i];
            if ($forceAsyncReloadEnabled || !$translationTable[fallbackLanguageId]) {
              langPromises[fallbackLanguageId] = loadAsync(fallbackLanguageId).then(processAsyncResult);
            }
          }
        }
      } else {
        $rootScope.$emit('$translateReady', { language: $translate.use() });
      }

      return $translate;
    }
  ];
}

$translate.displayName = 'displayName';

/**
 * @ngdoc object
 * @name pascalprecht.translate.$translateDefaultInterpolation
 * @requires $interpolate
 *
 * @description
 * Uses angular's `$interpolate` services to interpolate strings against some values.
 *
 * Be aware to configure a proper sanitization strategy.
 *
 * See also:
 * * {@link pascalprecht.translate.$translateSanitization}
 *
 * @return {object} $translateDefaultInterpolation Interpolator service
 */
angular.module('pascalprecht.translate').factory('$translateDefaultInterpolation', $translateDefaultInterpolation);

function $translateDefaultInterpolation ($interpolate, $translateSanitization) {

  'use strict';

  var $translateInterpolator = {},
      $locale,
      $identifier = 'default';

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateDefaultInterpolation#setLocale
   * @methodOf pascalprecht.translate.$translateDefaultInterpolation
   *
   * @description
   * Sets current locale (this is currently not use in this interpolation).
   *
   * @param {string} locale Language key or locale.
   */
  $translateInterpolator.setLocale = function (locale) {
    $locale = locale;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateDefaultInterpolation#getInterpolationIdentifier
   * @methodOf pascalprecht.translate.$translateDefaultInterpolation
   *
   * @description
   * Returns an identifier for this interpolation service.
   *
   * @returns {string} $identifier
   */
  $translateInterpolator.getInterpolationIdentifier = function () {
    return $identifier;
  };

  /**
   * @deprecated will be removed in 3.0
   * @see {@link pascalprecht.translate.$translateSanitization}
   */
  $translateInterpolator.useSanitizeValueStrategy = function (value) {
    $translateSanitization.useStrategy(value);
    return this;
  };

  /**
   * @ngdoc function
   * @name pascalprecht.translate.$translateDefaultInterpolation#interpolate
   * @methodOf pascalprecht.translate.$translateDefaultInterpolation
   *
   * @description
   * Interpolates given value agains given interpolate params using angulars
   * `$interpolate` service.
   *
   * Since AngularJS 1.5, `value` must not be a string but can be anything input.
   *
   * @returns {string} interpolated string.
   */
  $translateInterpolator.interpolate = function (value, interpolationParams) {
    interpolationParams = interpolationParams || {};
    interpolationParams = $translateSanitization.sanitize(interpolationParams, 'params');

    var interpolatedText;
    if (angular.isNumber(value)) {
      // numbers are safe
      interpolatedText = '' + value;
    } else if (angular.isString(value)) {
      // strings must be interpolated (that's the job here)
      interpolatedText = $interpolate(value)(interpolationParams);
      interpolatedText = $translateSanitization.sanitize(interpolatedText, 'text');
    } else {
      // neither a number or a string, cant interpolate => empty string
      interpolatedText = '';
    }

    return interpolatedText;
  };

  return $translateInterpolator;
}

$translateDefaultInterpolation.displayName = '$translateDefaultInterpolation';

angular.module('pascalprecht.translate').constant('$STORAGE_KEY', 'NG_TRANSLATE_LANG_KEY');

angular.module('pascalprecht.translate')
/**
 * @ngdoc directive
 * @name pascalprecht.translate.directive:translate
 * @requires $compile
 * @requires $filter
 * @requires $interpolate
 * @restrict AE
 *
 * @description
 * Translates given translation id either through attribute or DOM content.
 * Internally it uses `translate` filter to translate translation id. It possible to
 * pass an optional `translate-values` object literal as string into translation id.
 *
 * @param {string=} translate Translation id which could be either string or interpolated string.
 * @param {string=} translate-values Values to pass into translation id. Can be passed as object literal string or interpolated object.
 * @param {string=} translate-attr-ATTR translate Translation id and put it into ATTR attribute.
 * @param {string=} translate-default will be used unless translation was successful
 * @param {boolean=} translate-compile (default true if present) defines locally activation of {@link pascalprecht.translate.$translateProvider#methods_usePostCompiling}
 * @param {boolean=} translate-keep-content (default true if present) defines that in case a KEY could not be translated, that the existing content is left in the innerHTML}
 *
 * @example
   <example module="ngView">
    <file name="index.html">
      <div ng-controller="TranslateCtrl">

        <pre translate="TRANSLATION_ID"></pre>
        <pre translate>TRANSLATION_ID</pre>
        <pre translate translate-attr-title="TRANSLATION_ID"></pre>
        <pre translate="{{translationId}}"></pre>
        <pre translate>{{translationId}}</pre>
        <pre translate="WITH_VALUES" translate-values="{value: 5}"></pre>
        <pre translate translate-values="{value: 5}">WITH_VALUES</pre>
        <pre translate="WITH_VALUES" translate-values="{{values}}"></pre>
        <pre translate translate-values="{{values}}">WITH_VALUES</pre>
        <pre translate translate-attr-title="WITH_VALUES" translate-values="{{values}}"></pre>
        <pre translate="WITH_CAMEL_CASE_KEY" translate-value-camel-case-key="Hi"></pre>

      </div>
    </file>
    <file name="script.js">
      angular.module('ngView', ['pascalprecht.translate'])

      .config(function ($translateProvider) {

        $translateProvider.translations('en',{
          'TRANSLATION_ID': 'Hello there!',
          'WITH_VALUES': 'The following value is dynamic: {{value}}',
          'WITH_CAMEL_CASE_KEY': 'The interpolation key is camel cased: {{camelCaseKey}}'
        }).preferredLanguage('en');

      });

      angular.module('ngView').controller('TranslateCtrl', function ($scope) {
        $scope.translationId = 'TRANSLATION_ID';

        $scope.values = {
          value: 78
        };
      });
    </file>
    <file name="scenario.js">
      it('should translate', function () {
        inject(function ($rootScope, $compile) {
          $rootScope.translationId = 'TRANSLATION_ID';

          element = $compile('<p translate="TRANSLATION_ID"></p>')($rootScope);
          $rootScope.$digest();
          expect(element.text()).toBe('Hello there!');

          element = $compile('<p translate="{{translationId}}"></p>')($rootScope);
          $rootScope.$digest();
          expect(element.text()).toBe('Hello there!');

          element = $compile('<p translate>TRANSLATION_ID</p>')($rootScope);
          $rootScope.$digest();
          expect(element.text()).toBe('Hello there!');

          element = $compile('<p translate>{{translationId}}</p>')($rootScope);
          $rootScope.$digest();
          expect(element.text()).toBe('Hello there!');

          element = $compile('<p translate translate-attr-title="TRANSLATION_ID"></p>')($rootScope);
          $rootScope.$digest();
          expect(element.attr('title')).toBe('Hello there!');

          element = $compile('<p translate="WITH_CAMEL_CASE_KEY" translate-value-camel-case-key="Hello"></p>')($rootScope);
          $rootScope.$digest();
          expect(element.text()).toBe('The interpolation key is camel cased: Hello');
        });
      });
    </file>
   </example>
 */
.directive('translate', translateDirective);
function translateDirective($translate, $q, $interpolate, $compile, $parse, $rootScope) {

  'use strict';

  /**
   * @name trim
   * @private
   *
   * @description
   * trim polyfill
   *
   * @returns {string} The string stripped of whitespace from both ends
   */
  var trim = function() {
    return this.toString().replace(/^\s+|\s+$/g, '');
  };

  return {
    restrict: 'AE',
    scope: true,
    priority: $translate.directivePriority(),
    compile: function (tElement, tAttr) {

      var translateValuesExist = (tAttr.translateValues) ?
        tAttr.translateValues : undefined;

      var translateInterpolation = (tAttr.translateInterpolation) ?
        tAttr.translateInterpolation : undefined;

      var translateValueExist = tElement[0].outerHTML.match(/translate-value-+/i);

      var interpolateRegExp = '^(.*)(' + $interpolate.startSymbol() + '.*' + $interpolate.endSymbol() + ')(.*)',
          watcherRegExp = '^(.*)' + $interpolate.startSymbol() + '(.*)' + $interpolate.endSymbol() + '(.*)';

      return function linkFn(scope, iElement, iAttr) {

        scope.interpolateParams = {};
        scope.preText = '';
        scope.postText = '';
        scope.translateNamespace = getTranslateNamespace(scope);
        var translationIds = {};

        var initInterpolationParams = function (interpolateParams, iAttr, tAttr) {
          // initial setup
          if (iAttr.translateValues) {
            angular.extend(interpolateParams, $parse(iAttr.translateValues)(scope.$parent));
          }
          // initially fetch all attributes if existing and fill the params
          if (translateValueExist) {
            for (var attr in tAttr) {
              if (Object.prototype.hasOwnProperty.call(iAttr, attr) && attr.substr(0, 14) === 'translateValue' && attr !== 'translateValues') {
                var attributeName = angular.lowercase(attr.substr(14, 1)) + attr.substr(15);
                interpolateParams[attributeName] = tAttr[attr];
              }
            }
          }
        };

        // Ensures any change of the attribute "translate" containing the id will
        // be re-stored to the scope's "translationId".
        // If the attribute has no content, the element's text value (white spaces trimmed off) will be used.
        var observeElementTranslation = function (translationId) {

          // Remove any old watcher
          if (angular.isFunction(observeElementTranslation._unwatchOld)) {
            observeElementTranslation._unwatchOld();
            observeElementTranslation._unwatchOld = undefined;
          }

          if (angular.equals(translationId , '') || !angular.isDefined(translationId)) {
            var iElementText = trim.apply(iElement.text());

            // Resolve translation id by inner html if required
            var interpolateMatches = iElementText.match(interpolateRegExp);
            // Interpolate translation id if required
            if (angular.isArray(interpolateMatches)) {
              scope.preText = interpolateMatches[1];
              scope.postText = interpolateMatches[3];
              translationIds.translate = $interpolate(interpolateMatches[2])(scope.$parent);
              var watcherMatches = iElementText.match(watcherRegExp);
              if (angular.isArray(watcherMatches) && watcherMatches[2] && watcherMatches[2].length) {
                observeElementTranslation._unwatchOld = scope.$watch(watcherMatches[2], function (newValue) {
                  translationIds.translate = newValue;
                  updateTranslations();
                });
              }
            } else {
              // do not assigne the translation id if it is empty.
              translationIds.translate = !iElementText ? undefined : iElementText;
            }
          } else {
            translationIds.translate = translationId;
          }
          updateTranslations();
        };

        var observeAttributeTranslation = function (translateAttr) {
          iAttr.$observe(translateAttr, function (translationId) {
            translationIds[translateAttr] = translationId;
            updateTranslations();
          });
        };

        // initial setup with values
        initInterpolationParams(scope.interpolateParams, iAttr, tAttr);

        var firstAttributeChangedEvent = true;
        iAttr.$observe('translate', function (translationId) {
          if (typeof translationId === 'undefined') {
            // case of element "<translate>xyz</translate>"
            observeElementTranslation('');
          } else {
            // case of regular attribute
            if (translationId !== '' || !firstAttributeChangedEvent) {
              translationIds.translate = translationId;
              updateTranslations();
            }
          }
          firstAttributeChangedEvent = false;
        });

        for (var translateAttr in iAttr) {
          if (iAttr.hasOwnProperty(translateAttr) && translateAttr.substr(0, 13) === 'translateAttr') {
            observeAttributeTranslation(translateAttr);
          }
        }

        iAttr.$observe('translateDefault', function (value) {
          scope.defaultText = value;
          updateTranslations();
        });

        if (translateValuesExist) {
          iAttr.$observe('translateValues', function (interpolateParams) {
            if (interpolateParams) {
              scope.$parent.$watch(function () {
                angular.extend(scope.interpolateParams, $parse(interpolateParams)(scope.$parent));
              });
            }
          });
        }

        if (translateValueExist) {
          var observeValueAttribute = function (attrName) {
            iAttr.$observe(attrName, function (value) {
              var attributeName = angular.lowercase(attrName.substr(14, 1)) + attrName.substr(15);
              scope.interpolateParams[attributeName] = value;
            });
          };
          for (var attr in iAttr) {
            if (Object.prototype.hasOwnProperty.call(iAttr, attr) && attr.substr(0, 14) === 'translateValue' && attr !== 'translateValues') {
              observeValueAttribute(attr);
            }
          }
        }

        // Master update function
        var updateTranslations = function () {
          for (var key in translationIds) {
            if (translationIds.hasOwnProperty(key) && translationIds[key] !== undefined) {
              updateTranslation(key, translationIds[key], scope, scope.interpolateParams, scope.defaultText, scope.translateNamespace);
            }
          }
        };

        // Put translation processing function outside loop
        var updateTranslation = function(translateAttr, translationId, scope, interpolateParams, defaultTranslationText, translateNamespace) {
          if (translationId) {
            // if translation id starts with '.' and translateNamespace given, prepend namespace
            if (translateNamespace && translationId.charAt(0) === '.') {
              translationId = translateNamespace + translationId;
            }

            $translate(translationId, interpolateParams, translateInterpolation, defaultTranslationText, scope.translateLanguage)
              .then(function (translation) {
                applyTranslation(translation, scope, true, translateAttr);
              }, function (translationId) {
                applyTranslation(translationId, scope, false, translateAttr);
              });
          } else {
            // as an empty string cannot be translated, we can solve this using successful=false
            applyTranslation(translationId, scope, false, translateAttr);
          }
        };

        var applyTranslation = function (value, scope, successful, translateAttr) {
          if (!successful) {
            if (typeof scope.defaultText !== 'undefined') {
              value = scope.defaultText;
            }
          }
          if (translateAttr === 'translate') {
            // default translate into innerHTML
            if (successful || (!successful && !$translate.isKeepContent() && typeof iAttr.translateKeepContent === 'undefined')) {
              iElement.empty().append(scope.preText + value + scope.postText);
            }
            var globallyEnabled = $translate.isPostCompilingEnabled();
            var locallyDefined = typeof tAttr.translateCompile !== 'undefined';
            var locallyEnabled = locallyDefined && tAttr.translateCompile !== 'false';
            if ((globallyEnabled && !locallyDefined) || locallyEnabled) {
              $compile(iElement.contents())(scope);
            }
          } else {
            // translate attribute
            var attributeName = iAttr.$attr[translateAttr];
            if (attributeName.substr(0, 5) === 'data-') {
              // ensure html5 data prefix is stripped
              attributeName = attributeName.substr(5);
            }
            attributeName = attributeName.substr(15);
            iElement.attr(attributeName, value);
          }
        };

        if (translateValuesExist || translateValueExist || iAttr.translateDefault) {
          scope.$watch('interpolateParams', updateTranslations, true);
        }

        // Replaced watcher on translateLanguage with event listener
        var unbindTranslateLanguage = scope.$on('translateLanguageChanged', updateTranslations);

        // Ensures the text will be refreshed after the current language was changed
        // w/ $translate.use(...)
        var unbind = $rootScope.$on('$translateChangeSuccess', updateTranslations);

        // ensure translation will be looked up at least one
        if (iElement.text().length) {
          if (iAttr.translate) {
            observeElementTranslation(iAttr.translate);
          } else {
            observeElementTranslation('');
          }
        } else if (iAttr.translate) {
          // ensure attribute will be not skipped
          observeElementTranslation(iAttr.translate);
        }
        updateTranslations();
        scope.$on('$destroy', function(){
          unbindTranslateLanguage();
          unbind();
        });
      };
    }
  };
}

/**
 * Returns the scope's namespace.
 * @private
 * @param scope
 * @returns {string}
 */
function getTranslateNamespace(scope) {
  'use strict';
  if (scope.translateNamespace) {
    return scope.translateNamespace;
  }
  if (scope.$parent) {
    return getTranslateNamespace(scope.$parent);
  }
}

translateDirective.displayName = 'translateDirective';

angular.module('pascalprecht.translate')
/**
 * @ngdoc directive
 * @name pascalprecht.translate.directive:translateCloak
 * @requires $rootScope
 * @requires $translate
 * @restrict A
 *
 * $description
 * Adds a `translate-cloak` class name to the given element where this directive
 * is applied initially and removes it, once a loader has finished loading.
 *
 * This directive can be used to prevent initial flickering when loading translation
 * data asynchronously.
 *
 * The class name is defined in
 * {@link pascalprecht.translate.$translateProvider#cloakClassName $translate.cloakClassName()}.
 *
 * @param {string=} translate-cloak If a translationId is provided, it will be used for showing
 *                                  or hiding the cloak. Basically it relies on the translation
 *                                  resolve.
 */
.directive('translateCloak', translateCloakDirective);

function translateCloakDirective($translate, $rootScope) {

  'use strict';

  return {
    compile: function (tElement) {
      var applyCloak = function () {
        tElement.addClass($translate.cloakClassName());
      },
      removeCloak = function () {
        tElement.removeClass($translate.cloakClassName());
      };
      $translate.onReady(function () {
        removeCloak();
      });
      applyCloak();

      return function linkFn(scope, iElement, iAttr) {
        if (iAttr.translateCloak && iAttr.translateCloak.length) {
          // Register a watcher for the defined translation allowing a fine tuned cloak
          iAttr.$observe('translateCloak', function (translationId) {
            $translate(translationId).then(removeCloak, applyCloak);
          });
          // Register for change events as this is being another indicicator revalidating the cloak)
          $rootScope.$on('$translateChangeSuccess', function () {
            $translate(iAttr.translateCloak).then(removeCloak, applyCloak);
          });
        }
      };
    }
  };
}

translateCloakDirective.displayName = 'translateCloakDirective';

angular.module('pascalprecht.translate')
/**
 * @ngdoc directive
 * @name pascalprecht.translate.directive:translateNamespace
 * @restrict A
 *
 * @description
 * Translates given translation id either through attribute or DOM content.
 * Internally it uses `translate` filter to translate translation id. It possible to
 * pass an optional `translate-values` object literal as string into translation id.
 *
 * @param {string=} translate namespace name which could be either string or interpolated string.
 *
 * @example
   <example module="ngView">
    <file name="index.html">
      <div translate-namespace="CONTENT">

        <div>
            <h1 translate>.HEADERS.TITLE</h1>
            <h1 translate>.HEADERS.WELCOME</h1>
        </div>

        <div translate-namespace=".HEADERS">
            <h1 translate>.TITLE</h1>
            <h1 translate>.WELCOME</h1>
        </div>

      </div>
    </file>
    <file name="script.js">
      angular.module('ngView', ['pascalprecht.translate'])

      .config(function ($translateProvider) {

        $translateProvider.translations('en',{
          'TRANSLATION_ID': 'Hello there!',
          'CONTENT': {
            'HEADERS': {
                TITLE: 'Title'
            }
          },
          'CONTENT.HEADERS.WELCOME': 'Welcome'
        }).preferredLanguage('en');

      });

    </file>
   </example>
 */
.directive('translateNamespace', translateNamespaceDirective);

function translateNamespaceDirective() {

  'use strict';

  return {
    restrict: 'A',
    scope: true,
    compile: function () {
      return {
        pre: function (scope, iElement, iAttrs) {
          scope.translateNamespace = getTranslateNamespace(scope);

          if (scope.translateNamespace && iAttrs.translateNamespace.charAt(0) === '.') {
            scope.translateNamespace += iAttrs.translateNamespace;
          } else {
            scope.translateNamespace = iAttrs.translateNamespace;
          }
        }
      };
    }
  };
}

/**
 * Returns the scope's namespace.
 * @private
 * @param scope
 * @returns {string}
 */
function getTranslateNamespace(scope) {
  'use strict';
  if (scope.translateNamespace) {
    return scope.translateNamespace;
  }
  if (scope.$parent) {
    return getTranslateNamespace(scope.$parent);
  }
}

translateNamespaceDirective.displayName = 'translateNamespaceDirective';

angular.module('pascalprecht.translate')
/**
 * @ngdoc directive
 * @name pascalprecht.translate.directive:translateLanguage
 * @restrict A
 *
 * @description
 * Forces the language to the directives in the underlying scope.
 *
 * @param {string=} translate language that will be negotiated.
 *
 * @example
   <example module="ngView">
    <file name="index.html">
      <div>

        <div>
            <h1 translate>HELLO</h1>
        </div>

        <div translate-language="de">
            <h1 translate>HELLO</h1>
        </div>

      </div>
    </file>
    <file name="script.js">
      angular.module('ngView', ['pascalprecht.translate'])

      .config(function ($translateProvider) {

        $translateProvider
          .translations('en',{
            'HELLO': 'Hello world!'
          })
          .translations('de',{
            'HELLO': 'Hallo Welt!'
          })
          .preferredLanguage('en');

      });

    </file>
   </example>
 */
.directive('translateLanguage', translateLanguageDirective);

function translateLanguageDirective() {

  'use strict';

  return {
    restrict: 'A',
    scope: true,
    compile: function () {
      return function linkFn(scope, iElement, iAttrs) {

        iAttrs.$observe('translateLanguage', function (newTranslateLanguage) {
          scope.translateLanguage = newTranslateLanguage;
        });

        scope.$watch('translateLanguage', function(){
          scope.$broadcast('translateLanguageChanged');
        });
      };
    }
  };
}

translateLanguageDirective.displayName = 'translateLanguageDirective';

angular.module('pascalprecht.translate')
/**
 * @ngdoc filter
 * @name pascalprecht.translate.filter:translate
 * @requires $parse
 * @requires pascalprecht.translate.$translate
 * @function
 *
 * @description
 * Uses `$translate` service to translate contents. Accepts interpolate parameters
 * to pass dynamized values though translation.
 *
 * @param {string} translationId A translation id to be translated.
 * @param {*=} interpolateParams Optional object literal (as hash or string) to pass values into translation.
 *
 * @returns {string} Translated text.
 *
 * @example
   <example module="ngView">
    <file name="index.html">
      <div ng-controller="TranslateCtrl">

        <pre>{{ 'TRANSLATION_ID' | translate }}</pre>
        <pre>{{ translationId | translate }}</pre>
        <pre>{{ 'WITH_VALUES' | translate:'{value: 5}' }}</pre>
        <pre>{{ 'WITH_VALUES' | translate:values }}</pre>

      </div>
    </file>
    <file name="script.js">
      angular.module('ngView', ['pascalprecht.translate'])

      .config(function ($translateProvider) {

        $translateProvider.translations('en', {
          'TRANSLATION_ID': 'Hello there!',
          'WITH_VALUES': 'The following value is dynamic: {{value}}'
        });
        $translateProvider.preferredLanguage('en');

      });

      angular.module('ngView').controller('TranslateCtrl', function ($scope) {
        $scope.translationId = 'TRANSLATION_ID';

        $scope.values = {
          value: 78
        };
      });
    </file>
   </example>
 */
.filter('translate', translateFilterFactory);

function translateFilterFactory($parse, $translate) {

  'use strict';

  var translateFilter = function (translationId, interpolateParams, interpolation, forceLanguage) {
    if (!angular.isObject(interpolateParams)) {
      interpolateParams = $parse(interpolateParams)(this);
    }

    return $translate.instant(translationId, interpolateParams, interpolation, forceLanguage);
  };

  if ($translate.statefulFilter()) {
    translateFilter.$stateful = true;
  }

  return translateFilter;
}

translateFilterFactory.displayName = 'translateFilterFactory';

angular.module('pascalprecht.translate')

/**
 * @ngdoc object
 * @name pascalprecht.translate.$translationCache
 * @requires $cacheFactory
 *
 * @description
 * The first time a translation table is used, it is loaded in the translation cache for quick retrieval. You
 * can load translation tables directly into the cache by consuming the
 * `$translationCache` service directly.
 *
 * @return {object} $cacheFactory object.
 */
  .factory('$translationCache', $translationCache);

function $translationCache($cacheFactory) {

  'use strict';

  return $cacheFactory('translations');
}

$translationCache.displayName = '$translationCache';
return 'pascalprecht.translate';

}));
;/*!
 * Bootstrap v3.3.7 (http://getbootstrap.com)
 * Copyright 2011-2016 Twitter, Inc.
 * Licensed under the MIT license
 */
if("undefined"==typeof jQuery)throw new Error("Bootstrap's JavaScript requires jQuery");+function(a){"use strict";var b=a.fn.jquery.split(" ")[0].split(".");if(b[0]<2&&b[1]<9||1==b[0]&&9==b[1]&&b[2]<1||b[0]>3)throw new Error("Bootstrap's JavaScript requires jQuery version 1.9.1 or higher, but lower than version 4")}(jQuery),+function(a){"use strict";function b(){var a=document.createElement("bootstrap"),b={WebkitTransition:"webkitTransitionEnd",MozTransition:"transitionend",OTransition:"oTransitionEnd otransitionend",transition:"transitionend"};for(var c in b)if(void 0!==a.style[c])return{end:b[c]};return!1}a.fn.emulateTransitionEnd=function(b){var c=!1,d=this;a(this).one("bsTransitionEnd",function(){c=!0});var e=function(){c||a(d).trigger(a.support.transition.end)};return setTimeout(e,b),this},a(function(){a.support.transition=b(),a.support.transition&&(a.event.special.bsTransitionEnd={bindType:a.support.transition.end,delegateType:a.support.transition.end,handle:function(b){if(a(b.target).is(this))return b.handleObj.handler.apply(this,arguments)}})})}(jQuery),+function(a){"use strict";function b(b){return this.each(function(){var c=a(this),e=c.data("bs.alert");e||c.data("bs.alert",e=new d(this)),"string"==typeof b&&e[b].call(c)})}var c='[data-dismiss="alert"]',d=function(b){a(b).on("click",c,this.close)};d.VERSION="3.3.7",d.TRANSITION_DURATION=150,d.prototype.close=function(b){function c(){g.detach().trigger("closed.bs.alert").remove()}var e=a(this),f=e.attr("data-target");f||(f=e.attr("href"),f=f&&f.replace(/.*(?=#[^\s]*$)/,""));var g=a("#"===f?[]:f);b&&b.preventDefault(),g.length||(g=e.closest(".alert")),g.trigger(b=a.Event("close.bs.alert")),b.isDefaultPrevented()||(g.removeClass("in"),a.support.transition&&g.hasClass("fade")?g.one("bsTransitionEnd",c).emulateTransitionEnd(d.TRANSITION_DURATION):c())};var e=a.fn.alert;a.fn.alert=b,a.fn.alert.Constructor=d,a.fn.alert.noConflict=function(){return a.fn.alert=e,this},a(document).on("click.bs.alert.data-api",c,d.prototype.close)}(jQuery),+function(a){"use strict";function b(b){return this.each(function(){var d=a(this),e=d.data("bs.button"),f="object"==typeof b&&b;e||d.data("bs.button",e=new c(this,f)),"toggle"==b?e.toggle():b&&e.setState(b)})}var c=function(b,d){this.$element=a(b),this.options=a.extend({},c.DEFAULTS,d),this.isLoading=!1};c.VERSION="3.3.7",c.DEFAULTS={loadingText:"loading..."},c.prototype.setState=function(b){var c="disabled",d=this.$element,e=d.is("input")?"val":"html",f=d.data();b+="Text",null==f.resetText&&d.data("resetText",d[e]()),setTimeout(a.proxy(function(){d[e](null==f[b]?this.options[b]:f[b]),"loadingText"==b?(this.isLoading=!0,d.addClass(c).attr(c,c).prop(c,!0)):this.isLoading&&(this.isLoading=!1,d.removeClass(c).removeAttr(c).prop(c,!1))},this),0)},c.prototype.toggle=function(){var a=!0,b=this.$element.closest('[data-toggle="buttons"]');if(b.length){var c=this.$element.find("input");"radio"==c.prop("type")?(c.prop("checked")&&(a=!1),b.find(".active").removeClass("active"),this.$element.addClass("active")):"checkbox"==c.prop("type")&&(c.prop("checked")!==this.$element.hasClass("active")&&(a=!1),this.$element.toggleClass("active")),c.prop("checked",this.$element.hasClass("active")),a&&c.trigger("change")}else this.$element.attr("aria-pressed",!this.$element.hasClass("active")),this.$element.toggleClass("active")};var d=a.fn.button;a.fn.button=b,a.fn.button.Constructor=c,a.fn.button.noConflict=function(){return a.fn.button=d,this},a(document).on("click.bs.button.data-api",'[data-toggle^="button"]',function(c){var d=a(c.target).closest(".btn");b.call(d,"toggle"),a(c.target).is('input[type="radio"], input[type="checkbox"]')||(c.preventDefault(),d.is("input,button")?d.trigger("focus"):d.find("input:visible,button:visible").first().trigger("focus"))}).on("focus.bs.button.data-api blur.bs.button.data-api",'[data-toggle^="button"]',function(b){a(b.target).closest(".btn").toggleClass("focus",/^focus(in)?$/.test(b.type))})}(jQuery),+function(a){"use strict";function b(b){return this.each(function(){var d=a(this),e=d.data("bs.carousel"),f=a.extend({},c.DEFAULTS,d.data(),"object"==typeof b&&b),g="string"==typeof b?b:f.slide;e||d.data("bs.carousel",e=new c(this,f)),"number"==typeof b?e.to(b):g?e[g]():f.interval&&e.pause().cycle()})}var c=function(b,c){this.$element=a(b),this.$indicators=this.$element.find(".carousel-indicators"),this.options=c,this.paused=null,this.sliding=null,this.interval=null,this.$active=null,this.$items=null,this.options.keyboard&&this.$element.on("keydown.bs.carousel",a.proxy(this.keydown,this)),"hover"==this.options.pause&&!("ontouchstart"in document.documentElement)&&this.$element.on("mouseenter.bs.carousel",a.proxy(this.pause,this)).on("mouseleave.bs.carousel",a.proxy(this.cycle,this))};c.VERSION="3.3.7",c.TRANSITION_DURATION=600,c.DEFAULTS={interval:5e3,pause:"hover",wrap:!0,keyboard:!0},c.prototype.keydown=function(a){if(!/input|textarea/i.test(a.target.tagName)){switch(a.which){case 37:this.prev();break;case 39:this.next();break;default:return}a.preventDefault()}},c.prototype.cycle=function(b){return b||(this.paused=!1),this.interval&&clearInterval(this.interval),this.options.interval&&!this.paused&&(this.interval=setInterval(a.proxy(this.next,this),this.options.interval)),this},c.prototype.getItemIndex=function(a){return this.$items=a.parent().children(".item"),this.$items.index(a||this.$active)},c.prototype.getItemForDirection=function(a,b){var c=this.getItemIndex(b),d="prev"==a&&0===c||"next"==a&&c==this.$items.length-1;if(d&&!this.options.wrap)return b;var e="prev"==a?-1:1,f=(c+e)%this.$items.length;return this.$items.eq(f)},c.prototype.to=function(a){var b=this,c=this.getItemIndex(this.$active=this.$element.find(".item.active"));if(!(a>this.$items.length-1||a<0))return this.sliding?this.$element.one("slid.bs.carousel",function(){b.to(a)}):c==a?this.pause().cycle():this.slide(a>c?"next":"prev",this.$items.eq(a))},c.prototype.pause=function(b){return b||(this.paused=!0),this.$element.find(".next, .prev").length&&a.support.transition&&(this.$element.trigger(a.support.transition.end),this.cycle(!0)),this.interval=clearInterval(this.interval),this},c.prototype.next=function(){if(!this.sliding)return this.slide("next")},c.prototype.prev=function(){if(!this.sliding)return this.slide("prev")},c.prototype.slide=function(b,d){var e=this.$element.find(".item.active"),f=d||this.getItemForDirection(b,e),g=this.interval,h="next"==b?"left":"right",i=this;if(f.hasClass("active"))return this.sliding=!1;var j=f[0],k=a.Event("slide.bs.carousel",{relatedTarget:j,direction:h});if(this.$element.trigger(k),!k.isDefaultPrevented()){if(this.sliding=!0,g&&this.pause(),this.$indicators.length){this.$indicators.find(".active").removeClass("active");var l=a(this.$indicators.children()[this.getItemIndex(f)]);l&&l.addClass("active")}var m=a.Event("slid.bs.carousel",{relatedTarget:j,direction:h});return a.support.transition&&this.$element.hasClass("slide")?(f.addClass(b),f[0].offsetWidth,e.addClass(h),f.addClass(h),e.one("bsTransitionEnd",function(){f.removeClass([b,h].join(" ")).addClass("active"),e.removeClass(["active",h].join(" ")),i.sliding=!1,setTimeout(function(){i.$element.trigger(m)},0)}).emulateTransitionEnd(c.TRANSITION_DURATION)):(e.removeClass("active"),f.addClass("active"),this.sliding=!1,this.$element.trigger(m)),g&&this.cycle(),this}};var d=a.fn.carousel;a.fn.carousel=b,a.fn.carousel.Constructor=c,a.fn.carousel.noConflict=function(){return a.fn.carousel=d,this};var e=function(c){var d,e=a(this),f=a(e.attr("data-target")||(d=e.attr("href"))&&d.replace(/.*(?=#[^\s]+$)/,""));if(f.hasClass("carousel")){var g=a.extend({},f.data(),e.data()),h=e.attr("data-slide-to");h&&(g.interval=!1),b.call(f,g),h&&f.data("bs.carousel").to(h),c.preventDefault()}};a(document).on("click.bs.carousel.data-api","[data-slide]",e).on("click.bs.carousel.data-api","[data-slide-to]",e),a(window).on("load",function(){a('[data-ride="carousel"]').each(function(){var c=a(this);b.call(c,c.data())})})}(jQuery),+function(a){"use strict";function b(b){var c,d=b.attr("data-target")||(c=b.attr("href"))&&c.replace(/.*(?=#[^\s]+$)/,"");return a(d)}function c(b){return this.each(function(){var c=a(this),e=c.data("bs.collapse"),f=a.extend({},d.DEFAULTS,c.data(),"object"==typeof b&&b);!e&&f.toggle&&/show|hide/.test(b)&&(f.toggle=!1),e||c.data("bs.collapse",e=new d(this,f)),"string"==typeof b&&e[b]()})}var d=function(b,c){this.$element=a(b),this.options=a.extend({},d.DEFAULTS,c),this.$trigger=a('[data-toggle="collapse"][href="#'+b.id+'"],[data-toggle="collapse"][data-target="#'+b.id+'"]'),this.transitioning=null,this.options.parent?this.$parent=this.getParent():this.addAriaAndCollapsedClass(this.$element,this.$trigger),this.options.toggle&&this.toggle()};d.VERSION="3.3.7",d.TRANSITION_DURATION=350,d.DEFAULTS={toggle:!0},d.prototype.dimension=function(){var a=this.$element.hasClass("width");return a?"width":"height"},d.prototype.show=function(){if(!this.transitioning&&!this.$element.hasClass("in")){var b,e=this.$parent&&this.$parent.children(".panel").children(".in, .collapsing");if(!(e&&e.length&&(b=e.data("bs.collapse"),b&&b.transitioning))){var f=a.Event("show.bs.collapse");if(this.$element.trigger(f),!f.isDefaultPrevented()){e&&e.length&&(c.call(e,"hide"),b||e.data("bs.collapse",null));var g=this.dimension();this.$element.removeClass("collapse").addClass("collapsing")[g](0).attr("aria-expanded",!0),this.$trigger.removeClass("collapsed").attr("aria-expanded",!0),this.transitioning=1;var h=function(){this.$element.removeClass("collapsing").addClass("collapse in")[g](""),this.transitioning=0,this.$element.trigger("shown.bs.collapse")};if(!a.support.transition)return h.call(this);var i=a.camelCase(["scroll",g].join("-"));this.$element.one("bsTransitionEnd",a.proxy(h,this)).emulateTransitionEnd(d.TRANSITION_DURATION)[g](this.$element[0][i])}}}},d.prototype.hide=function(){if(!this.transitioning&&this.$element.hasClass("in")){var b=a.Event("hide.bs.collapse");if(this.$element.trigger(b),!b.isDefaultPrevented()){var c=this.dimension();this.$element[c](this.$element[c]())[0].offsetHeight,this.$element.addClass("collapsing").removeClass("collapse in").attr("aria-expanded",!1),this.$trigger.addClass("collapsed").attr("aria-expanded",!1),this.transitioning=1;var e=function(){this.transitioning=0,this.$element.removeClass("collapsing").addClass("collapse").trigger("hidden.bs.collapse")};return a.support.transition?void this.$element[c](0).one("bsTransitionEnd",a.proxy(e,this)).emulateTransitionEnd(d.TRANSITION_DURATION):e.call(this)}}},d.prototype.toggle=function(){this[this.$element.hasClass("in")?"hide":"show"]()},d.prototype.getParent=function(){return a(this.options.parent).find('[data-toggle="collapse"][data-parent="'+this.options.parent+'"]').each(a.proxy(function(c,d){var e=a(d);this.addAriaAndCollapsedClass(b(e),e)},this)).end()},d.prototype.addAriaAndCollapsedClass=function(a,b){var c=a.hasClass("in");a.attr("aria-expanded",c),b.toggleClass("collapsed",!c).attr("aria-expanded",c)};var e=a.fn.collapse;a.fn.collapse=c,a.fn.collapse.Constructor=d,a.fn.collapse.noConflict=function(){return a.fn.collapse=e,this},a(document).on("click.bs.collapse.data-api",'[data-toggle="collapse"]',function(d){var e=a(this);e.attr("data-target")||d.preventDefault();var f=b(e),g=f.data("bs.collapse"),h=g?"toggle":e.data();c.call(f,h)})}(jQuery),+function(a){"use strict";function b(b){var c=b.attr("data-target");c||(c=b.attr("href"),c=c&&/#[A-Za-z]/.test(c)&&c.replace(/.*(?=#[^\s]*$)/,""));var d=c&&a(c);return d&&d.length?d:b.parent()}function c(c){c&&3===c.which||(a(e).remove(),a(f).each(function(){var d=a(this),e=b(d),f={relatedTarget:this};e.hasClass("open")&&(c&&"click"==c.type&&/input|textarea/i.test(c.target.tagName)&&a.contains(e[0],c.target)||(e.trigger(c=a.Event("hide.bs.dropdown",f)),c.isDefaultPrevented()||(d.attr("aria-expanded","false"),e.removeClass("open").trigger(a.Event("hidden.bs.dropdown",f)))))}))}function d(b){return this.each(function(){var c=a(this),d=c.data("bs.dropdown");d||c.data("bs.dropdown",d=new g(this)),"string"==typeof b&&d[b].call(c)})}var e=".dropdown-backdrop",f='[data-toggle="dropdown"]',g=function(b){a(b).on("click.bs.dropdown",this.toggle)};g.VERSION="3.3.7",g.prototype.toggle=function(d){var e=a(this);if(!e.is(".disabled, :disabled")){var f=b(e),g=f.hasClass("open");if(c(),!g){"ontouchstart"in document.documentElement&&!f.closest(".navbar-nav").length&&a(document.createElement("div")).addClass("dropdown-backdrop").insertAfter(a(this)).on("click",c);var h={relatedTarget:this};if(f.trigger(d=a.Event("show.bs.dropdown",h)),d.isDefaultPrevented())return;e.trigger("focus").attr("aria-expanded","true"),f.toggleClass("open").trigger(a.Event("shown.bs.dropdown",h))}return!1}},g.prototype.keydown=function(c){if(/(38|40|27|32)/.test(c.which)&&!/input|textarea/i.test(c.target.tagName)){var d=a(this);if(c.preventDefault(),c.stopPropagation(),!d.is(".disabled, :disabled")){var e=b(d),g=e.hasClass("open");if(!g&&27!=c.which||g&&27==c.which)return 27==c.which&&e.find(f).trigger("focus"),d.trigger("click");var h=" li:not(.disabled):visible a",i=e.find(".dropdown-menu"+h);if(i.length){var j=i.index(c.target);38==c.which&&j>0&&j--,40==c.which&&j<i.length-1&&j++,~j||(j=0),i.eq(j).trigger("focus")}}}};var h=a.fn.dropdown;a.fn.dropdown=d,a.fn.dropdown.Constructor=g,a.fn.dropdown.noConflict=function(){return a.fn.dropdown=h,this},a(document).on("click.bs.dropdown.data-api",c).on("click.bs.dropdown.data-api",".dropdown form",function(a){a.stopPropagation()}).on("click.bs.dropdown.data-api",f,g.prototype.toggle).on("keydown.bs.dropdown.data-api",f,g.prototype.keydown).on("keydown.bs.dropdown.data-api",".dropdown-menu",g.prototype.keydown)}(jQuery),+function(a){"use strict";function b(b,d){return this.each(function(){var e=a(this),f=e.data("bs.modal"),g=a.extend({},c.DEFAULTS,e.data(),"object"==typeof b&&b);f||e.data("bs.modal",f=new c(this,g)),"string"==typeof b?f[b](d):g.show&&f.show(d)})}var c=function(b,c){this.options=c,this.$body=a(document.body),this.$element=a(b),this.$dialog=this.$element.find(".modal-dialog"),this.$backdrop=null,this.isShown=null,this.originalBodyPad=null,this.scrollbarWidth=0,this.ignoreBackdropClick=!1,this.options.remote&&this.$element.find(".modal-content").load(this.options.remote,a.proxy(function(){this.$element.trigger("loaded.bs.modal")},this))};c.VERSION="3.3.7",c.TRANSITION_DURATION=300,c.BACKDROP_TRANSITION_DURATION=150,c.DEFAULTS={backdrop:!0,keyboard:!0,show:!0},c.prototype.toggle=function(a){return this.isShown?this.hide():this.show(a)},c.prototype.show=function(b){var d=this,e=a.Event("show.bs.modal",{relatedTarget:b});this.$element.trigger(e),this.isShown||e.isDefaultPrevented()||(this.isShown=!0,this.checkScrollbar(),this.setScrollbar(),this.$body.addClass("modal-open"),this.escape(),this.resize(),this.$element.on("click.dismiss.bs.modal",'[data-dismiss="modal"]',a.proxy(this.hide,this)),this.$dialog.on("mousedown.dismiss.bs.modal",function(){d.$element.one("mouseup.dismiss.bs.modal",function(b){a(b.target).is(d.$element)&&(d.ignoreBackdropClick=!0)})}),this.backdrop(function(){var e=a.support.transition&&d.$element.hasClass("fade");d.$element.parent().length||d.$element.appendTo(d.$body),d.$element.show().scrollTop(0),d.adjustDialog(),e&&d.$element[0].offsetWidth,d.$element.addClass("in"),d.enforceFocus();var f=a.Event("shown.bs.modal",{relatedTarget:b});e?d.$dialog.one("bsTransitionEnd",function(){d.$element.trigger("focus").trigger(f)}).emulateTransitionEnd(c.TRANSITION_DURATION):d.$element.trigger("focus").trigger(f)}))},c.prototype.hide=function(b){b&&b.preventDefault(),b=a.Event("hide.bs.modal"),this.$element.trigger(b),this.isShown&&!b.isDefaultPrevented()&&(this.isShown=!1,this.escape(),this.resize(),a(document).off("focusin.bs.modal"),this.$element.removeClass("in").off("click.dismiss.bs.modal").off("mouseup.dismiss.bs.modal"),this.$dialog.off("mousedown.dismiss.bs.modal"),a.support.transition&&this.$element.hasClass("fade")?this.$element.one("bsTransitionEnd",a.proxy(this.hideModal,this)).emulateTransitionEnd(c.TRANSITION_DURATION):this.hideModal())},c.prototype.enforceFocus=function(){a(document).off("focusin.bs.modal").on("focusin.bs.modal",a.proxy(function(a){document===a.target||this.$element[0]===a.target||this.$element.has(a.target).length||this.$element.trigger("focus")},this))},c.prototype.escape=function(){this.isShown&&this.options.keyboard?this.$element.on("keydown.dismiss.bs.modal",a.proxy(function(a){27==a.which&&this.hide()},this)):this.isShown||this.$element.off("keydown.dismiss.bs.modal")},c.prototype.resize=function(){this.isShown?a(window).on("resize.bs.modal",a.proxy(this.handleUpdate,this)):a(window).off("resize.bs.modal")},c.prototype.hideModal=function(){var a=this;this.$element.hide(),this.backdrop(function(){a.$body.removeClass("modal-open"),a.resetAdjustments(),a.resetScrollbar(),a.$element.trigger("hidden.bs.modal")})},c.prototype.removeBackdrop=function(){this.$backdrop&&this.$backdrop.remove(),this.$backdrop=null},c.prototype.backdrop=function(b){var d=this,e=this.$element.hasClass("fade")?"fade":"";if(this.isShown&&this.options.backdrop){var f=a.support.transition&&e;if(this.$backdrop=a(document.createElement("div")).addClass("modal-backdrop "+e).appendTo(this.$body),this.$element.on("click.dismiss.bs.modal",a.proxy(function(a){return this.ignoreBackdropClick?void(this.ignoreBackdropClick=!1):void(a.target===a.currentTarget&&("static"==this.options.backdrop?this.$element[0].focus():this.hide()))},this)),f&&this.$backdrop[0].offsetWidth,this.$backdrop.addClass("in"),!b)return;f?this.$backdrop.one("bsTransitionEnd",b).emulateTransitionEnd(c.BACKDROP_TRANSITION_DURATION):b()}else if(!this.isShown&&this.$backdrop){this.$backdrop.removeClass("in");var g=function(){d.removeBackdrop(),b&&b()};a.support.transition&&this.$element.hasClass("fade")?this.$backdrop.one("bsTransitionEnd",g).emulateTransitionEnd(c.BACKDROP_TRANSITION_DURATION):g()}else b&&b()},c.prototype.handleUpdate=function(){this.adjustDialog()},c.prototype.adjustDialog=function(){var a=this.$element[0].scrollHeight>document.documentElement.clientHeight;this.$element.css({paddingLeft:!this.bodyIsOverflowing&&a?this.scrollbarWidth:"",paddingRight:this.bodyIsOverflowing&&!a?this.scrollbarWidth:""})},c.prototype.resetAdjustments=function(){this.$element.css({paddingLeft:"",paddingRight:""})},c.prototype.checkScrollbar=function(){var a=window.innerWidth;if(!a){var b=document.documentElement.getBoundingClientRect();a=b.right-Math.abs(b.left)}this.bodyIsOverflowing=document.body.clientWidth<a,this.scrollbarWidth=this.measureScrollbar()},c.prototype.setScrollbar=function(){var a=parseInt(this.$body.css("padding-right")||0,10);this.originalBodyPad=document.body.style.paddingRight||"",this.bodyIsOverflowing&&this.$body.css("padding-right",a+this.scrollbarWidth)},c.prototype.resetScrollbar=function(){this.$body.css("padding-right",this.originalBodyPad)},c.prototype.measureScrollbar=function(){var a=document.createElement("div");a.className="modal-scrollbar-measure",this.$body.append(a);var b=a.offsetWidth-a.clientWidth;return this.$body[0].removeChild(a),b};var d=a.fn.modal;a.fn.modal=b,a.fn.modal.Constructor=c,a.fn.modal.noConflict=function(){return a.fn.modal=d,this},a(document).on("click.bs.modal.data-api",'[data-toggle="modal"]',function(c){var d=a(this),e=d.attr("href"),f=a(d.attr("data-target")||e&&e.replace(/.*(?=#[^\s]+$)/,"")),g=f.data("bs.modal")?"toggle":a.extend({remote:!/#/.test(e)&&e},f.data(),d.data());d.is("a")&&c.preventDefault(),f.one("show.bs.modal",function(a){a.isDefaultPrevented()||f.one("hidden.bs.modal",function(){d.is(":visible")&&d.trigger("focus")})}),b.call(f,g,this)})}(jQuery),+function(a){"use strict";function b(b){return this.each(function(){var d=a(this),e=d.data("bs.tooltip"),f="object"==typeof b&&b;!e&&/destroy|hide/.test(b)||(e||d.data("bs.tooltip",e=new c(this,f)),"string"==typeof b&&e[b]())})}var c=function(a,b){this.type=null,this.options=null,this.enabled=null,this.timeout=null,this.hoverState=null,this.$element=null,this.inState=null,this.init("tooltip",a,b)};c.VERSION="3.3.7",c.TRANSITION_DURATION=150,c.DEFAULTS={animation:!0,placement:"top",selector:!1,template:'<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',trigger:"hover focus",title:"",delay:0,html:!1,container:!1,viewport:{selector:"body",padding:0}},c.prototype.init=function(b,c,d){if(this.enabled=!0,this.type=b,this.$element=a(c),this.options=this.getOptions(d),this.$viewport=this.options.viewport&&a(a.isFunction(this.options.viewport)?this.options.viewport.call(this,this.$element):this.options.viewport.selector||this.options.viewport),this.inState={click:!1,hover:!1,focus:!1},this.$element[0]instanceof document.constructor&&!this.options.selector)throw new Error("`selector` option must be specified when initializing "+this.type+" on the window.document object!");for(var e=this.options.trigger.split(" "),f=e.length;f--;){var g=e[f];if("click"==g)this.$element.on("click."+this.type,this.options.selector,a.proxy(this.toggle,this));else if("manual"!=g){var h="hover"==g?"mouseenter":"focusin",i="hover"==g?"mouseleave":"focusout";this.$element.on(h+"."+this.type,this.options.selector,a.proxy(this.enter,this)),this.$element.on(i+"."+this.type,this.options.selector,a.proxy(this.leave,this))}}this.options.selector?this._options=a.extend({},this.options,{trigger:"manual",selector:""}):this.fixTitle()},c.prototype.getDefaults=function(){return c.DEFAULTS},c.prototype.getOptions=function(b){return b=a.extend({},this.getDefaults(),this.$element.data(),b),b.delay&&"number"==typeof b.delay&&(b.delay={show:b.delay,hide:b.delay}),b},c.prototype.getDelegateOptions=function(){var b={},c=this.getDefaults();return this._options&&a.each(this._options,function(a,d){c[a]!=d&&(b[a]=d)}),b},c.prototype.enter=function(b){var c=b instanceof this.constructor?b:a(b.currentTarget).data("bs."+this.type);return c||(c=new this.constructor(b.currentTarget,this.getDelegateOptions()),a(b.currentTarget).data("bs."+this.type,c)),b instanceof a.Event&&(c.inState["focusin"==b.type?"focus":"hover"]=!0),c.tip().hasClass("in")||"in"==c.hoverState?void(c.hoverState="in"):(clearTimeout(c.timeout),c.hoverState="in",c.options.delay&&c.options.delay.show?void(c.timeout=setTimeout(function(){"in"==c.hoverState&&c.show()},c.options.delay.show)):c.show())},c.prototype.isInStateTrue=function(){for(var a in this.inState)if(this.inState[a])return!0;return!1},c.prototype.leave=function(b){var c=b instanceof this.constructor?b:a(b.currentTarget).data("bs."+this.type);if(c||(c=new this.constructor(b.currentTarget,this.getDelegateOptions()),a(b.currentTarget).data("bs."+this.type,c)),b instanceof a.Event&&(c.inState["focusout"==b.type?"focus":"hover"]=!1),!c.isInStateTrue())return clearTimeout(c.timeout),c.hoverState="out",c.options.delay&&c.options.delay.hide?void(c.timeout=setTimeout(function(){"out"==c.hoverState&&c.hide()},c.options.delay.hide)):c.hide()},c.prototype.show=function(){var b=a.Event("show.bs."+this.type);if(this.hasContent()&&this.enabled){this.$element.trigger(b);var d=a.contains(this.$element[0].ownerDocument.documentElement,this.$element[0]);if(b.isDefaultPrevented()||!d)return;var e=this,f=this.tip(),g=this.getUID(this.type);this.setContent(),f.attr("id",g),this.$element.attr("aria-describedby",g),this.options.animation&&f.addClass("fade");var h="function"==typeof this.options.placement?this.options.placement.call(this,f[0],this.$element[0]):this.options.placement,i=/\s?auto?\s?/i,j=i.test(h);j&&(h=h.replace(i,"")||"top"),f.detach().css({top:0,left:0,display:"block"}).addClass(h).data("bs."+this.type,this),this.options.container?f.appendTo(this.options.container):f.insertAfter(this.$element),this.$element.trigger("inserted.bs."+this.type);var k=this.getPosition(),l=f[0].offsetWidth,m=f[0].offsetHeight;if(j){var n=h,o=this.getPosition(this.$viewport);h="bottom"==h&&k.bottom+m>o.bottom?"top":"top"==h&&k.top-m<o.top?"bottom":"right"==h&&k.right+l>o.width?"left":"left"==h&&k.left-l<o.left?"right":h,f.removeClass(n).addClass(h)}var p=this.getCalculatedOffset(h,k,l,m);this.applyPlacement(p,h);var q=function(){var a=e.hoverState;e.$element.trigger("shown.bs."+e.type),e.hoverState=null,"out"==a&&e.leave(e)};a.support.transition&&this.$tip.hasClass("fade")?f.one("bsTransitionEnd",q).emulateTransitionEnd(c.TRANSITION_DURATION):q()}},c.prototype.applyPlacement=function(b,c){var d=this.tip(),e=d[0].offsetWidth,f=d[0].offsetHeight,g=parseInt(d.css("margin-top"),10),h=parseInt(d.css("margin-left"),10);isNaN(g)&&(g=0),isNaN(h)&&(h=0),b.top+=g,b.left+=h,a.offset.setOffset(d[0],a.extend({using:function(a){d.css({top:Math.round(a.top),left:Math.round(a.left)})}},b),0),d.addClass("in");var i=d[0].offsetWidth,j=d[0].offsetHeight;"top"==c&&j!=f&&(b.top=b.top+f-j);var k=this.getViewportAdjustedDelta(c,b,i,j);k.left?b.left+=k.left:b.top+=k.top;var l=/top|bottom/.test(c),m=l?2*k.left-e+i:2*k.top-f+j,n=l?"offsetWidth":"offsetHeight";d.offset(b),this.replaceArrow(m,d[0][n],l)},c.prototype.replaceArrow=function(a,b,c){this.arrow().css(c?"left":"top",50*(1-a/b)+"%").css(c?"top":"left","")},c.prototype.setContent=function(){var a=this.tip(),b=this.getTitle();a.find(".tooltip-inner")[this.options.html?"html":"text"](b),a.removeClass("fade in top bottom left right")},c.prototype.hide=function(b){function d(){"in"!=e.hoverState&&f.detach(),e.$element&&e.$element.removeAttr("aria-describedby").trigger("hidden.bs."+e.type),b&&b()}var e=this,f=a(this.$tip),g=a.Event("hide.bs."+this.type);if(this.$element.trigger(g),!g.isDefaultPrevented())return f.removeClass("in"),a.support.transition&&f.hasClass("fade")?f.one("bsTransitionEnd",d).emulateTransitionEnd(c.TRANSITION_DURATION):d(),this.hoverState=null,this},c.prototype.fixTitle=function(){var a=this.$element;(a.attr("title")||"string"!=typeof a.attr("data-original-title"))&&a.attr("data-original-title",a.attr("title")||"").attr("title","")},c.prototype.hasContent=function(){return this.getTitle()},c.prototype.getPosition=function(b){b=b||this.$element;var c=b[0],d="BODY"==c.tagName,e=c.getBoundingClientRect();null==e.width&&(e=a.extend({},e,{width:e.right-e.left,height:e.bottom-e.top}));var f=window.SVGElement&&c instanceof window.SVGElement,g=d?{top:0,left:0}:f?null:b.offset(),h={scroll:d?document.documentElement.scrollTop||document.body.scrollTop:b.scrollTop()},i=d?{width:a(window).width(),height:a(window).height()}:null;return a.extend({},e,h,i,g)},c.prototype.getCalculatedOffset=function(a,b,c,d){return"bottom"==a?{top:b.top+b.height,left:b.left+b.width/2-c/2}:"top"==a?{top:b.top-d,left:b.left+b.width/2-c/2}:"left"==a?{top:b.top+b.height/2-d/2,left:b.left-c}:{top:b.top+b.height/2-d/2,left:b.left+b.width}},c.prototype.getViewportAdjustedDelta=function(a,b,c,d){var e={top:0,left:0};if(!this.$viewport)return e;var f=this.options.viewport&&this.options.viewport.padding||0,g=this.getPosition(this.$viewport);if(/right|left/.test(a)){var h=b.top-f-g.scroll,i=b.top+f-g.scroll+d;h<g.top?e.top=g.top-h:i>g.top+g.height&&(e.top=g.top+g.height-i)}else{var j=b.left-f,k=b.left+f+c;j<g.left?e.left=g.left-j:k>g.right&&(e.left=g.left+g.width-k)}return e},c.prototype.getTitle=function(){var a,b=this.$element,c=this.options;return a=b.attr("data-original-title")||("function"==typeof c.title?c.title.call(b[0]):c.title)},c.prototype.getUID=function(a){do a+=~~(1e6*Math.random());while(document.getElementById(a));return a},c.prototype.tip=function(){if(!this.$tip&&(this.$tip=a(this.options.template),1!=this.$tip.length))throw new Error(this.type+" `template` option must consist of exactly 1 top-level element!");return this.$tip},c.prototype.arrow=function(){return this.$arrow=this.$arrow||this.tip().find(".tooltip-arrow")},c.prototype.enable=function(){this.enabled=!0},c.prototype.disable=function(){this.enabled=!1},c.prototype.toggleEnabled=function(){this.enabled=!this.enabled},c.prototype.toggle=function(b){var c=this;b&&(c=a(b.currentTarget).data("bs."+this.type),c||(c=new this.constructor(b.currentTarget,this.getDelegateOptions()),a(b.currentTarget).data("bs."+this.type,c))),b?(c.inState.click=!c.inState.click,c.isInStateTrue()?c.enter(c):c.leave(c)):c.tip().hasClass("in")?c.leave(c):c.enter(c)},c.prototype.destroy=function(){var a=this;clearTimeout(this.timeout),this.hide(function(){a.$element.off("."+a.type).removeData("bs."+a.type),a.$tip&&a.$tip.detach(),a.$tip=null,a.$arrow=null,a.$viewport=null,a.$element=null})};var d=a.fn.tooltip;a.fn.tooltip=b,a.fn.tooltip.Constructor=c,a.fn.tooltip.noConflict=function(){return a.fn.tooltip=d,this}}(jQuery),+function(a){"use strict";function b(b){return this.each(function(){var d=a(this),e=d.data("bs.popover"),f="object"==typeof b&&b;!e&&/destroy|hide/.test(b)||(e||d.data("bs.popover",e=new c(this,f)),"string"==typeof b&&e[b]())})}var c=function(a,b){this.init("popover",a,b)};if(!a.fn.tooltip)throw new Error("Popover requires tooltip.js");c.VERSION="3.3.7",c.DEFAULTS=a.extend({},a.fn.tooltip.Constructor.DEFAULTS,{placement:"right",trigger:"click",content:"",template:'<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'}),c.prototype=a.extend({},a.fn.tooltip.Constructor.prototype),c.prototype.constructor=c,c.prototype.getDefaults=function(){return c.DEFAULTS},c.prototype.setContent=function(){var a=this.tip(),b=this.getTitle(),c=this.getContent();a.find(".popover-title")[this.options.html?"html":"text"](b),a.find(".popover-content").children().detach().end()[this.options.html?"string"==typeof c?"html":"append":"text"](c),a.removeClass("fade top bottom left right in"),a.find(".popover-title").html()||a.find(".popover-title").hide()},c.prototype.hasContent=function(){return this.getTitle()||this.getContent()},c.prototype.getContent=function(){var a=this.$element,b=this.options;return a.attr("data-content")||("function"==typeof b.content?b.content.call(a[0]):b.content)},c.prototype.arrow=function(){return this.$arrow=this.$arrow||this.tip().find(".arrow")};var d=a.fn.popover;a.fn.popover=b,a.fn.popover.Constructor=c,a.fn.popover.noConflict=function(){return a.fn.popover=d,this}}(jQuery),+function(a){"use strict";function b(c,d){this.$body=a(document.body),this.$scrollElement=a(a(c).is(document.body)?window:c),this.options=a.extend({},b.DEFAULTS,d),this.selector=(this.options.target||"")+" .nav li > a",this.offsets=[],this.targets=[],this.activeTarget=null,this.scrollHeight=0,this.$scrollElement.on("scroll.bs.scrollspy",a.proxy(this.process,this)),this.refresh(),this.process()}function c(c){return this.each(function(){var d=a(this),e=d.data("bs.scrollspy"),f="object"==typeof c&&c;e||d.data("bs.scrollspy",e=new b(this,f)),"string"==typeof c&&e[c]()})}b.VERSION="3.3.7",b.DEFAULTS={offset:10},b.prototype.getScrollHeight=function(){return this.$scrollElement[0].scrollHeight||Math.max(this.$body[0].scrollHeight,document.documentElement.scrollHeight)},b.prototype.refresh=function(){var b=this,c="offset",d=0;this.offsets=[],this.targets=[],this.scrollHeight=this.getScrollHeight(),a.isWindow(this.$scrollElement[0])||(c="position",d=this.$scrollElement.scrollTop()),this.$body.find(this.selector).map(function(){var b=a(this),e=b.data("target")||b.attr("href"),f=/^#./.test(e)&&a(e);return f&&f.length&&f.is(":visible")&&[[f[c]().top+d,e]]||null}).sort(function(a,b){return a[0]-b[0]}).each(function(){b.offsets.push(this[0]),b.targets.push(this[1])})},b.prototype.process=function(){var a,b=this.$scrollElement.scrollTop()+this.options.offset,c=this.getScrollHeight(),d=this.options.offset+c-this.$scrollElement.height(),e=this.offsets,f=this.targets,g=this.activeTarget;if(this.scrollHeight!=c&&this.refresh(),b>=d)return g!=(a=f[f.length-1])&&this.activate(a);if(g&&b<e[0])return this.activeTarget=null,this.clear();for(a=e.length;a--;)g!=f[a]&&b>=e[a]&&(void 0===e[a+1]||b<e[a+1])&&this.activate(f[a])},b.prototype.activate=function(b){
this.activeTarget=b,this.clear();var c=this.selector+'[data-target="'+b+'"],'+this.selector+'[href="'+b+'"]',d=a(c).parents("li").addClass("active");d.parent(".dropdown-menu").length&&(d=d.closest("li.dropdown").addClass("active")),d.trigger("activate.bs.scrollspy")},b.prototype.clear=function(){a(this.selector).parentsUntil(this.options.target,".active").removeClass("active")};var d=a.fn.scrollspy;a.fn.scrollspy=c,a.fn.scrollspy.Constructor=b,a.fn.scrollspy.noConflict=function(){return a.fn.scrollspy=d,this},a(window).on("load.bs.scrollspy.data-api",function(){a('[data-spy="scroll"]').each(function(){var b=a(this);c.call(b,b.data())})})}(jQuery),+function(a){"use strict";function b(b){return this.each(function(){var d=a(this),e=d.data("bs.tab");e||d.data("bs.tab",e=new c(this)),"string"==typeof b&&e[b]()})}var c=function(b){this.element=a(b)};c.VERSION="3.3.7",c.TRANSITION_DURATION=150,c.prototype.show=function(){var b=this.element,c=b.closest("ul:not(.dropdown-menu)"),d=b.data("target");if(d||(d=b.attr("href"),d=d&&d.replace(/.*(?=#[^\s]*$)/,"")),!b.parent("li").hasClass("active")){var e=c.find(".active:last a"),f=a.Event("hide.bs.tab",{relatedTarget:b[0]}),g=a.Event("show.bs.tab",{relatedTarget:e[0]});if(e.trigger(f),b.trigger(g),!g.isDefaultPrevented()&&!f.isDefaultPrevented()){var h=a(d);this.activate(b.closest("li"),c),this.activate(h,h.parent(),function(){e.trigger({type:"hidden.bs.tab",relatedTarget:b[0]}),b.trigger({type:"shown.bs.tab",relatedTarget:e[0]})})}}},c.prototype.activate=function(b,d,e){function f(){g.removeClass("active").find("> .dropdown-menu > .active").removeClass("active").end().find('[data-toggle="tab"]').attr("aria-expanded",!1),b.addClass("active").find('[data-toggle="tab"]').attr("aria-expanded",!0),h?(b[0].offsetWidth,b.addClass("in")):b.removeClass("fade"),b.parent(".dropdown-menu").length&&b.closest("li.dropdown").addClass("active").end().find('[data-toggle="tab"]').attr("aria-expanded",!0),e&&e()}var g=d.find("> .active"),h=e&&a.support.transition&&(g.length&&g.hasClass("fade")||!!d.find("> .fade").length);g.length&&h?g.one("bsTransitionEnd",f).emulateTransitionEnd(c.TRANSITION_DURATION):f(),g.removeClass("in")};var d=a.fn.tab;a.fn.tab=b,a.fn.tab.Constructor=c,a.fn.tab.noConflict=function(){return a.fn.tab=d,this};var e=function(c){c.preventDefault(),b.call(a(this),"show")};a(document).on("click.bs.tab.data-api",'[data-toggle="tab"]',e).on("click.bs.tab.data-api",'[data-toggle="pill"]',e)}(jQuery),+function(a){"use strict";function b(b){return this.each(function(){var d=a(this),e=d.data("bs.affix"),f="object"==typeof b&&b;e||d.data("bs.affix",e=new c(this,f)),"string"==typeof b&&e[b]()})}var c=function(b,d){this.options=a.extend({},c.DEFAULTS,d),this.$target=a(this.options.target).on("scroll.bs.affix.data-api",a.proxy(this.checkPosition,this)).on("click.bs.affix.data-api",a.proxy(this.checkPositionWithEventLoop,this)),this.$element=a(b),this.affixed=null,this.unpin=null,this.pinnedOffset=null,this.checkPosition()};c.VERSION="3.3.7",c.RESET="affix affix-top affix-bottom",c.DEFAULTS={offset:0,target:window},c.prototype.getState=function(a,b,c,d){var e=this.$target.scrollTop(),f=this.$element.offset(),g=this.$target.height();if(null!=c&&"top"==this.affixed)return e<c&&"top";if("bottom"==this.affixed)return null!=c?!(e+this.unpin<=f.top)&&"bottom":!(e+g<=a-d)&&"bottom";var h=null==this.affixed,i=h?e:f.top,j=h?g:b;return null!=c&&e<=c?"top":null!=d&&i+j>=a-d&&"bottom"},c.prototype.getPinnedOffset=function(){if(this.pinnedOffset)return this.pinnedOffset;this.$element.removeClass(c.RESET).addClass("affix");var a=this.$target.scrollTop(),b=this.$element.offset();return this.pinnedOffset=b.top-a},c.prototype.checkPositionWithEventLoop=function(){setTimeout(a.proxy(this.checkPosition,this),1)},c.prototype.checkPosition=function(){if(this.$element.is(":visible")){var b=this.$element.height(),d=this.options.offset,e=d.top,f=d.bottom,g=Math.max(a(document).height(),a(document.body).height());"object"!=typeof d&&(f=e=d),"function"==typeof e&&(e=d.top(this.$element)),"function"==typeof f&&(f=d.bottom(this.$element));var h=this.getState(g,b,e,f);if(this.affixed!=h){null!=this.unpin&&this.$element.css("top","");var i="affix"+(h?"-"+h:""),j=a.Event(i+".bs.affix");if(this.$element.trigger(j),j.isDefaultPrevented())return;this.affixed=h,this.unpin="bottom"==h?this.getPinnedOffset():null,this.$element.removeClass(c.RESET).addClass(i).trigger(i.replace("affix","affixed")+".bs.affix")}"bottom"==h&&this.$element.offset({top:g-b-f})}};var d=a.fn.affix;a.fn.affix=b,a.fn.affix.Constructor=c,a.fn.affix.noConflict=function(){return a.fn.affix=d,this},a(window).on("load",function(){a('[data-spy="affix"]').each(function(){var c=a(this),d=c.data();d.offset=d.offset||{},null!=d.offsetBottom&&(d.offset.bottom=d.offsetBottom),null!=d.offsetTop&&(d.offset.top=d.offsetTop),b.call(c,d)})})}(jQuery);;/*!
angular-xeditable - 0.1.12
Edit-in-place for angular.js
Build date: 2016-04-14 
*/
angular.module("xeditable",[]).value("editableOptions",{theme:"default",icon_set:"default",buttons:"right",blurElem:"cancel",blurForm:"ignore",activate:"focus",isDisabled:!1,activationEvent:"click"}),angular.module("xeditable").directive("editableBsdate",["editableDirectiveFactory",function(a){return a({directiveName:"editableBsdate",inputTpl:"<div></div>",render:function(){this.parent.render.call(this);var a=angular.element('<input type="text" class="form-control" ng-model="$data"/>'),b=angular.element('<button type="button" class="btn btn-default"><i class="glyphicon glyphicon-calendar"></i></button>'),c=angular.element('<span class="input-group-btn"></span>');a.attr("uib-datepicker-popup",this.attrs.eDatepickerPopupXEditable||"yyyy/MM/dd"),a.attr("is-open",this.attrs.eIsOpen),a.attr("date-disabled",this.attrs.eDateDisabled),a.attr("uib-datepicker-popup",this.attrs.eDatepickerPopup),a.attr("min-date",this.attrs.eMinDate),a.attr("max-date",this.attrs.eMaxDate),a.attr("year-range",this.attrs.eYearRange||20),a.attr("show-button-bar",this.attrs.eShowButtonBar||!0),a.attr("current-text",this.attrs.eCurrentText||"Today"),a.attr("clear-text",this.attrs.eClearText||"Clear"),a.attr("close-text",this.attrs.eCloseText||"Done"),a.attr("close-on-date-selection",this.attrs.eCloseOnDateSelection||!0),a.attr("datepicker-append-to-body",this.attrs.eDatePickerAppendToBody||!1),a.attr("date-disabled",this.attrs.eDateDisabled),a.attr("name",this.attrs.eName),this.scope.dateOptions={formatDay:this.attrs.eFormatDay||"dd",formatMonth:this.attrs.eFormatMonth||"MMMM",formatYear:this.attrs.eFormatYear||"yyyy",formatDayHeader:this.attrs.eFormatDayHeader||"EEE",formatDayTitle:this.attrs.eFormatDayTitle||"MMMM yyyy",formatMonthTitle:this.attrs.eFormatMonthTitle||"yyyy",showWeeks:this.attrs.eShowWeeks?"true"===this.attrs.eShowWeeks.toLowerCase():!0,startingDay:this.attrs.eStartingDay||0,minMode:this.attrs.eMinMode||"day",maxMode:this.attrs.eMaxMode||"year",initDate:this.attrs.eInitDate||new Date,datepickerMode:this.attrs.eDatepickerMode||"day"},a.attr("datepicker-options","dateOptions"),b.attr("ng-click",this.attrs.eNgClick),c.append(b),this.inputEl.prepend(a),this.inputEl.append(c),this.inputEl.removeAttr("class"),this.inputEl.removeAttr("ng-click"),this.inputEl.removeAttr("is-open"),this.inputEl.removeAttr("init-date"),this.inputEl.removeAttr("datepicker-popup"),this.inputEl.removeAttr("required"),this.inputEl.removeAttr("ng-model"),this.inputEl.removeAttr("date-picker-append-to-body"),this.inputEl.removeAttr("name"),this.inputEl.attr("class","input-group")}})}]),angular.module("xeditable").directive("editableBstime",["editableDirectiveFactory",function(a){return a({directiveName:"editableBstime",inputTpl:"<uib-timepicker></uib-timepicker>",render:function(){this.parent.render.call(this);var a=angular.element('<div class="well well-small" style="display:inline-block;"></div>');a.attr("ng-model",this.inputEl.attr("ng-model")),this.inputEl.removeAttr("ng-model"),this.attrs.eNgChange&&(a.attr("ng-change",this.inputEl.attr("ng-change")),this.inputEl.removeAttr("ng-change")),this.inputEl.wrap(a)}})}]),angular.module("xeditable").directive("editableCheckbox",["editableDirectiveFactory",function(a){return a({directiveName:"editableCheckbox",inputTpl:'<input type="checkbox">',render:function(){this.parent.render.call(this),this.attrs.eTitle&&(this.inputEl.wrap("<label></label>"),this.inputEl.parent().append(this.attrs.eTitle))},autosubmit:function(){var a=this;a.inputEl.bind("change",function(){setTimeout(function(){a.scope.$apply(function(){a.scope.$form.$submit()})},500)})}})}]),angular.module("xeditable").directive("editableChecklist",["editableDirectiveFactory","editableNgOptionsParser",function(a,b){return a({directiveName:"editableChecklist",inputTpl:"<span></span>",useCopy:!0,render:function(){this.parent.render.call(this);var a=b(this.attrs.eNgOptions),c='<label ng-repeat="'+a.ngRepeat+'"><input type="checkbox" checklist-model="$parent.$data" checklist-value="'+a.locals.valueFn+'"><span ng-bind="'+a.locals.displayFn+'"></span></label>';this.inputEl.removeAttr("ng-model"),this.inputEl.removeAttr("ng-options"),this.inputEl.html(c)}})}]),angular.module("xeditable").directive("editableCombodate",["editableDirectiveFactory","editableCombodate",function(a,b){return a({directiveName:"editableCombodate",inputTpl:'<input type="text">',render:function(){this.parent.render.call(this);var a={value:new Date(this.scope.$data)},c=this;angular.forEach(["format","template","minYear","maxYear","yearDescending","minuteStep","secondStep","firstItem","errorClass","customClass","roundTime","smartDays"],function(b){var d="e"+b.charAt(0).toUpperCase()+b.slice(1);d in c.attrs&&(a[b]=c.attrs[d])});var d=b.getInstance(this.inputEl,a);d.$widget.find("select").bind("change",function(a){c.scope.$data=new Date(d.getValue()).toISOString()})}})}]),function(){var a="text|password|email|tel|number|url|search|color|date|datetime|time|month|week|file".split("|");angular.forEach(a,function(a){var b="editable"+a.charAt(0).toUpperCase()+a.slice(1);angular.module("xeditable").directive(b,["editableDirectiveFactory",function(c){return c({directiveName:b,inputTpl:'<input type="'+a+'">'})}])}),angular.module("xeditable").directive("editableRange",["editableDirectiveFactory",function(a){return a({directiveName:"editableRange",inputTpl:'<input type="range" id="range" name="range">',render:function(){this.parent.render.call(this),this.inputEl.after("<output>{{$data}}</output>")}})}])}(),angular.module("xeditable").directive("editableRadiolist",["editableDirectiveFactory","editableNgOptionsParser",function(a,b){return a({directiveName:"editableRadiolist",inputTpl:"<span></span>",render:function(){this.parent.render.call(this);var a=b(this.attrs.eNgOptions),c='<label ng-repeat="'+a.ngRepeat+'"><input type="radio" ng-disabled="'+this.attrs.eNgDisabled+'" ng-model="$parent.$data" value="{{'+a.locals.valueFn+'}}"><span ng-bind="'+a.locals.displayFn+'"></span></label>';this.inputEl.removeAttr("ng-model"),this.inputEl.removeAttr("ng-options"),this.inputEl.html(c)},autosubmit:function(){var a=this;a.inputEl.bind("change",function(){setTimeout(function(){a.scope.$apply(function(){a.scope.$form.$submit()})},500)})}})}]),angular.module("xeditable").directive("editableSelect",["editableDirectiveFactory",function(a){return a({directiveName:"editableSelect",inputTpl:"<select></select>",autosubmit:function(){var a=this;a.inputEl.bind("change",function(){a.scope.$apply(function(){a.scope.$form.$submit()})})}})}]),angular.module("xeditable").directive("editableTextarea",["editableDirectiveFactory",function(a){return a({directiveName:"editableTextarea",inputTpl:"<textarea></textarea>",addListeners:function(){var a=this;a.parent.addListeners.call(a),a.single&&"no"!==a.buttons&&a.autosubmit()},autosubmit:function(){var a=this;a.inputEl.bind("keydown",function(b){(b.ctrlKey||b.metaKey)&&13===b.keyCode&&a.scope.$apply(function(){a.scope.$form.$submit()})})}})}]),angular.module("xeditable").directive("editableUiSelect",["editableDirectiveFactory",function(a){var b=function(a,b){var c=angular.element("<"+a+"/>");c.html(b.html());for(var d=b[0].attributes,e=0;e<d.length;++e)c.attr(d.item(e).nodeName,d.item(e).value);return c},c=null,d=null,e=a({directiveName:"editableUiSelect",inputTpl:"<ui-select></ui-select>",render:function(){this.parent.render.call(this),this.inputEl.append(b("ui-select-match",c)),this.inputEl.append(b("ui-select-choices",d)),this.inputEl.removeAttr("ng-model"),this.inputEl.attr("ng-model","$parent.$data")}}),f=e.link;return e.link=function(a,b,e,g){var h=b.find("editable-ui-select-match"),i=b.find("editable-ui-select-choices");return c=h.clone(),d=i.clone(),h.remove(),i.remove(),f(a,b,e,g)},e}]),angular.module("xeditable").factory("editableController",["$q","editableUtils",function(a,b){function c(a,c,d,e,f,g,h,i,j,k){var l,m,n=this;n.scope=a,n.elem=d,n.attrs=c,n.inputEl=null,n.editorEl=null,n.single=!0,n.error="",n.theme=f[h.theme]||f["default"],n.parent={},n.icon_set="default"===h.icon_set?g["default"][h.theme]:g.external[h.icon_set],n.inputTpl="",n.directiveName="",n.useCopy=!1,n.single=null,n.buttons="right",n.init=function(b){if(n.single=b,n.name=c.eName||c[n.directiveName],!c[n.directiveName])throw"You should provide value for `"+n.directiveName+"` in editable element!";l=e(c[n.directiveName]),n.single?n.buttons=n.attrs.buttons||h.buttons:n.buttons="no",c.eName&&n.scope.$watch("$data",function(a){n.scope.$form.$data[c.eName]=a}),c.onshow&&(n.onshow=function(){return n.catchError(e(c.onshow)(a))}),c.onhide&&(n.onhide=function(){return e(c.onhide)(a)}),c.oncancel&&(n.oncancel=function(){return e(c.oncancel)(a)}),c.onbeforesave&&(n.onbeforesave=function(){return n.catchError(e(c.onbeforesave)(a))}),c.onaftersave&&(n.onaftersave=function(){return n.catchError(e(c.onaftersave)(a))}),a.$parent.$watch(c[n.directiveName],function(a,b){n.setLocalValue(),n.handleEmpty()})},n.render=function(){var a=n.theme;n.inputEl=angular.element(n.inputTpl),n.controlsEl=angular.element(a.controlsTpl),n.controlsEl.append(n.inputEl),"no"!==n.buttons&&(n.buttonsEl=angular.element(a.buttonsTpl),n.submitEl=angular.element(a.submitTpl),n.cancelEl=angular.element(a.cancelTpl),n.icon_set&&(n.submitEl.find("span").addClass(n.icon_set.ok),n.cancelEl.find("span").addClass(n.icon_set.cancel)),n.buttonsEl.append(n.submitEl).append(n.cancelEl),n.controlsEl.append(n.buttonsEl),n.inputEl.addClass("editable-has-buttons")),n.errorEl=angular.element(a.errorTpl),n.controlsEl.append(n.errorEl),n.editorEl=angular.element(n.single?a.formTpl:a.noformTpl),n.editorEl.append(n.controlsEl);for(var d in c.$attr)if(!(d.length<=1)){var e=!1,f=d.substring(1,2);if("e"===d.substring(0,1)&&f===f.toUpperCase()&&(e=d.substring(1),"Form"!==e&&"NgSubmit"!==e)){e=e.substring(0,1).toLowerCase()+b.camelToDash(e.substring(1));var g="value"!==e&&""===c[d]?e:c[d];n.inputEl.attr(e,g)}}n.inputEl.addClass("editable-input"),n.inputEl.attr("ng-model","$data"),n.editorEl.addClass(b.camelToDash(n.directiveName)),n.single&&(n.editorEl.attr("editable-form","$form"),n.editorEl.attr("blur",n.attrs.blur||("no"===n.buttons?"cancel":h.blurElem))),angular.isFunction(a.postrender)&&a.postrender.call(n)},n.setLocalValue=function(){n.scope.$data=n.useCopy?angular.copy(l(a.$parent)):l(a.$parent)},n.show=function(){return n.setLocalValue(),n.render(),d.after(n.editorEl),j(n.editorEl)(a),n.addListeners(),d.addClass("editable-hide"),n.onshow()},n.hide=function(){return n.editorEl.remove(),d.removeClass("editable-hide"),n.onhide()},n.cancel=function(){n.oncancel()},n.addListeners=function(){n.inputEl.bind("keyup",function(a){if(n.single)switch(a.keyCode){case 27:n.scope.$apply(function(){n.scope.$form.$cancel()})}}),n.single&&"no"===n.buttons&&n.autosubmit(),n.editorEl.bind("click",function(a){a.which&&1!==a.which||n.scope.$form.$visible&&(n.scope.$form._clicked=!0)})},n.setWaiting=function(a){a?(m=!n.inputEl.attr("disabled")&&!n.inputEl.attr("ng-disabled")&&!n.inputEl.attr("ng-enabled"),m&&(n.inputEl.attr("disabled","disabled"),n.buttonsEl&&n.buttonsEl.find("button").attr("disabled","disabled"))):m&&(n.inputEl.removeAttr("disabled"),n.buttonsEl&&n.buttonsEl.find("button").removeAttr("disabled"))},n.activate=function(a,b){setTimeout(function(){var c=n.inputEl[0];"focus"===h.activate&&c.focus&&(a&&(b=b||a,c.onfocus=function(){var c=this;setTimeout(function(){c.setSelectionRange(a,b)})}),c.focus()),"select"===h.activate&&c.select&&c.select()},0)},n.setError=function(b){angular.isObject(b)||(a.$error=b,n.error=b)},n.catchError=function(a,b){return angular.isObject(a)&&b!==!0?k.when(a).then(angular.bind(this,function(a){this.catchError(a,!0)}),angular.bind(this,function(a){this.catchError(a,!0)})):b&&angular.isObject(a)&&a.status&&200!==a.status&&a.data&&angular.isString(a.data)?(this.setError(a.data),a=a.data):angular.isString(a)&&this.setError(a),a},n.save=function(){l.assign(a.$parent,n.useCopy?angular.copy(n.scope.$data):n.scope.$data)},n.handleEmpty=function(){var b=l(a.$parent),c=null===b||void 0===b||""===b||angular.isArray(b)&&0===b.length;d.toggleClass("editable-empty",c)},n.autosubmit=angular.noop,n.onshow=angular.noop,n.onhide=angular.noop,n.oncancel=angular.noop,n.onbeforesave=angular.noop,n.onaftersave=angular.noop}return c.$inject=["$scope","$attrs","$element","$parse","editableThemes","editableIcons","editableOptions","$rootScope","$compile","$q"],c}]),angular.module("xeditable").factory("editableDirectiveFactory",["$parse","$compile","editableThemes","$rootScope","$document","editableController","editableFormController","editableOptions",function(a,b,c,d,e,f,g,h){return function(b){return{restrict:"A",scope:!0,require:[b.directiveName,"?^form"],controller:f,link:function(c,f,i,j){var k,l=j[0],m=!1;if(j[1])k=j[1],m=void 0===i.eSingle;else if(i.eForm){var n=a(i.eForm)(c);if(n)k=n,m=!0;else for(var o=0;o<e[0].forms.length;o++)if(e[0].forms[o].name===i.eForm){k=null,m=!0;break}}angular.forEach(b,function(a,b){void 0!==l[b]&&(l.parent[b]=l[b])}),angular.extend(l,b);var p=angular.isDefined(i.editDisabled)?c.$eval(i.editDisabled):h.isDisabled;if(!p)if(l.init(!m),c.$editable=l,f.addClass("editable"),m)if(k){if(c.$form=k,!c.$form.$addEditable)throw"Form with editable elements should have `editable-form` attribute.";c.$form.$addEditable(l)}else d.$$editableBuffer=d.$$editableBuffer||{},d.$$editableBuffer[i.eForm]=d.$$editableBuffer[i.eForm]||[],d.$$editableBuffer[i.eForm].push(l),c.$form=null;else c.$form=g(),c.$form.$addEditable(l),i.eForm&&(c.$parent[i.eForm]=c.$form),(!i.eForm||i.eClickable)&&(f.addClass("editable-click"),f.bind(h.activationEvent,function(a){a.preventDefault(),a.editable=l,c.$apply(function(){c.$form.$show()})}))}}}}]),angular.module("xeditable").factory("editableFormController",["$parse","$document","$rootScope","editablePromiseCollection","editableUtils",function(a,b,c,d,e){var f=[],g=function(a,b){if(b==a)return!0;for(var c=b.parentNode;null!==c;){if(c==a)return!0;c=c.parentNode}return!1},h=function(a,b){var c=!0,d=a.$editables;return angular.forEach(d,function(a){var d=a.editorEl[0];g(d,b.target)&&(c=!1)}),c};b.bind("click",function(a){if(!a.which||1===a.which){for(var b=[],d=[],e=0;e<f.length;e++)f[e]._clicked?f[e]._clicked=!1:f[e].$waiting||("cancel"===f[e]._blur&&h(f[e],a)&&b.push(f[e]),"submit"===f[e]._blur&&h(f[e],a)&&d.push(f[e]));(b.length||d.length)&&c.$apply(function(){angular.forEach(b,function(a){a.$cancel()}),angular.forEach(d,function(a){a.$submit()})})}}),c.$on("closeEdit",function(){for(var a=0;a<f.length;a++)f[a].$hide()});var i={$addEditable:function(a){this.$editables.push(a),a.elem.bind("$destroy",angular.bind(this,this.$removeEditable,a)),a.scope.$form||(a.scope.$form=this),this.$visible&&a.catchError(a.show()),a.catchError(a.setWaiting(this.$waiting))},$removeEditable:function(a){for(var b=0;b<this.$editables.length;b++)if(this.$editables[b]===a)return void this.$editables.splice(b,1)},$show:function(){if(!this.$visible){this.$visible=!0;var a=d();a.when(this.$onshow()),this.$setError(null,""),angular.forEach(this.$editables,function(b){a.when(b.show())}),a.then({onWait:angular.bind(this,this.$setWaiting),onTrue:angular.bind(this,this.$activate),onFalse:angular.bind(this,this.$activate),onString:angular.bind(this,this.$activate)}),setTimeout(angular.bind(this,function(){this._clicked=!1,-1===e.indexOf(f,this)&&f.push(this)}),0)}},$activate:function(a){var b;if(this.$editables.length){if(angular.isString(a))for(b=0;b<this.$editables.length;b++)if(this.$editables[b].name===a)return void this.$editables[b].activate();for(b=0;b<this.$editables.length;b++)if(this.$editables[b].error)return void this.$editables[b].activate();this.$editables[0].activate(this.$editables[0].elem[0].selectionStart,this.$editables[0].elem[0].selectionEnd)}},$hide:function(){this.$visible&&(this.$visible=!1,this.$onhide(),angular.forEach(this.$editables,function(a){a.hide()}),e.arrayRemove(f,this))},$cancel:function(){this.$visible&&(this.$oncancel(),angular.forEach(this.$editables,function(a){a.cancel()}),this.$hide())},$setWaiting:function(a){this.$waiting=!!a,angular.forEach(this.$editables,function(b){b.setWaiting(!!a)})},$setError:function(a,b){angular.forEach(this.$editables,function(c){a&&c.name!==a||c.setError(b)})},$submit:function(){function a(a){var b=d();b.when(this.$onbeforesave()),b.then({onWait:angular.bind(this,this.$setWaiting),onTrue:a?angular.bind(this,this.$save):angular.bind(this,this.$hide),onFalse:angular.bind(this,this.$hide),onString:angular.bind(this,this.$activate)})}if(!this.$waiting){this.$setError(null,"");var b=d();angular.forEach(this.$editables,function(a){b.when(a.onbeforesave())}),b.then({onWait:angular.bind(this,this.$setWaiting),onTrue:angular.bind(this,a,!0),onFalse:angular.bind(this,a,!1),onString:angular.bind(this,this.$activate)})}},$save:function(){angular.forEach(this.$editables,function(a){a.save()});var a=d();a.when(this.$onaftersave()),angular.forEach(this.$editables,function(b){a.when(b.onaftersave())}),a.then({onWait:angular.bind(this,this.$setWaiting),onTrue:angular.bind(this,this.$hide),onFalse:angular.bind(this,this.$hide),onString:angular.bind(this,this.$activate)})},$onshow:angular.noop,$oncancel:angular.noop,$onhide:angular.noop,$onbeforesave:angular.noop,$onaftersave:angular.noop};return function(){return angular.extend({$editables:[],$visible:!1,$waiting:!1,$data:{},_clicked:!1,_blur:null},i)}}]),angular.module("xeditable").directive("editableForm",["$rootScope","$parse","editableFormController","editableOptions",function(a,b,c,d){return{restrict:"A",require:["form"],compile:function(){return{pre:function(b,d,e,f){var g,h=f[0];e.editableForm?b[e.editableForm]&&b[e.editableForm].$show?(g=b[e.editableForm],angular.extend(h,g)):(g=c(),b[e.editableForm]=g,angular.extend(g,h)):(g=c(),angular.extend(h,g));var i=a.$$editableBuffer,j=h.$name;j&&i&&i[j]&&(angular.forEach(i[j],function(a){g.$addEditable(a)}),delete i[j])},post:function(a,c,e,f){var g;g=e.editableForm&&a[e.editableForm]&&a[e.editableForm].$show?a[e.editableForm]:f[0],e.onshow&&(g.$onshow=angular.bind(g,b(e.onshow),a)),e.onhide&&(g.$onhide=angular.bind(g,b(e.onhide),a)),e.oncancel&&(g.$oncancel=angular.bind(g,b(e.oncancel),a)),e.shown&&b(e.shown)(a)&&g.$show(),g._blur=e.blur||d.blurForm,e.ngSubmit||e.submit||(e.onbeforesave&&(g.$onbeforesave=function(){return b(e.onbeforesave)(a,{$data:g.$data})}),e.onaftersave&&(g.$onaftersave=function(){return b(e.onaftersave)(a,{$data:g.$data})}),c.bind("submit",function(b){b.preventDefault(),a.$apply(function(){g.$submit()})})),c.bind("click",function(a){a.which&&1!==a.which||g.$visible&&(g._clicked=!0)})}}}}}]),angular.module("xeditable").factory("editablePromiseCollection",["$q",function(a){function b(){return{promises:[],hasFalse:!1,hasString:!1,when:function(b,c){if(b===!1)this.hasFalse=!0;else if(!c&&angular.isObject(b))this.promises.push(a.when(b));else{if(!angular.isString(b))return;this.hasString=!0}},then:function(b){function c(){h.hasString||h.hasFalse?!h.hasString&&h.hasFalse?e():f():d()}b=b||{};var d=b.onTrue||angular.noop,e=b.onFalse||angular.noop,f=b.onString||angular.noop,g=b.onWait||angular.noop,h=this;this.promises.length?(g(!0),a.all(this.promises).then(function(a){g(!1),angular.forEach(a,function(a){h.when(a,!0)}),c()},function(a){g(!1),f()})):c()}}}return b}]),angular.module("xeditable").factory("editableUtils",[function(){return{indexOf:function(a,b){if(a.indexOf)return a.indexOf(b);for(var c=0;c<a.length;c++)if(b===a[c])return c;return-1},arrayRemove:function(a,b){var c=this.indexOf(a,b);return c>=0&&a.splice(c,1),b},camelToDash:function(a){var b=/[A-Z]/g;return a.replace(b,function(a,b){return(b?"-":"")+a.toLowerCase()})},dashToCamel:function(a){var b=/([\:\-\_]+(.))/g,c=/^moz([A-Z])/;return a.replace(b,function(a,b,c,d){return d?c.toUpperCase():c}).replace(c,"Moz$1")}}}]),angular.module("xeditable").factory("editableNgOptionsParser",[function(){function a(a){var c;if(!(c=a.match(b)))throw"ng-options parse error";var d,e=c[2]||c[1],f=c[4]||c[6],g=c[5],h=(c[3]||"",c[2]?c[1]:f),i=c[7],j=c[8],k=j?c[8]:null;return void 0===g?(d=f+" in "+i,void 0!==j&&(d+=" track by "+k)):d="("+g+", "+f+") in "+i,{ngRepeat:d,locals:{valueName:f,keyName:g,valueFn:h,displayFn:e}}}var b=/^\s*(.*?)(?:\s+as\s+(.*?))?(?:\s+group\s+by\s+(.*))?\s+for\s+(?:([\$\w][\$\w]*)|(?:\(\s*([\$\w][\$\w]*)\s*,\s*([\$\w][\$\w]*)\s*\)))\s+in\s+(.*?)(?:\s+track\s+by\s+(.*?))?$/;return a}]),angular.module("xeditable").factory("editableCombodate",[function(){function a(a,b){if(this.$element=angular.element(a),"INPUT"!=this.$element[0].nodeName)throw"Combodate should be applied to INPUT element";var c=(new Date).getFullYear();this.defaults={format:"YYYY-MM-DD HH:mm",template:"D / MMM / YYYY   H : mm",value:null,minYear:1970,maxYear:c,yearDescending:!0,minuteStep:5,secondStep:1,firstItem:"empty",errorClass:null,customClass:"",roundTime:!0,smartDays:!0},this.options=angular.extend({},this.defaults,b),this.init()}return a.prototype={constructor:a,init:function(){if(this.map={day:["D","date"],month:["M","month"],year:["Y","year"],hour:["[Hh]","hours"],minute:["m","minutes"],second:["s","seconds"],ampm:["[Aa]",""]},this.$widget=angular.element('<span class="combodate"></span>').html(this.getTemplate()),this.initCombos(),this.options.smartDays){var a=this;this.$widget.find("select").bind("change",function(b){(angular.element(b.target).hasClass("month")||angular.element(b.target).hasClass("year"))&&a.fillCombo("day")})}this.$widget.find("select").css("width","auto"),this.$element.css("display","none").after(this.$widget),this.setValue(this.$element.val()||this.options.value)},getTemplate:function(){var a=this.options.template,b=this.options.customClass;return angular.forEach(this.map,function(b,c){b=b[0];var d=new RegExp(b+"+"),e=b.length>1?b.substring(1,2):b;a=a.replace(d,"{"+e+"}")}),a=a.replace(/ /g,"&nbsp;"),angular.forEach(this.map,function(c,d){c=c[0];var e=c.length>1?c.substring(1,2):c;a=a.replace("{"+e+"}",'<select class="'+d+" "+b+'"></select>')}),a},initCombos:function(){for(var a in this.map){var b=this.$widget[0].querySelectorAll("."+a);this["$"+a]=b.length?angular.element(b):null,this.fillCombo(a)}},fillCombo:function(a){var b=this["$"+a];if(b){var c="fill"+a.charAt(0).toUpperCase()+a.slice(1),d=this[c](),e=b.val();b.html("");for(var f=0;f<d.length;f++)b.append('<option value="'+d[f][0]+'">'+d[f][1]+"</option>");b.val(e)}},fillCommon:function(a){var b,c=[];if("name"===this.options.firstItem){b=moment.relativeTime||moment.langData()._relativeTime;var d="function"==typeof b[a]?b[a](1,!0,a,!1):b[a];d=d.split(" ").reverse()[0],c.push(["",d])}else"empty"===this.options.firstItem&&c.push(["",""]);return c},fillDay:function(){var a,b,c=this.fillCommon("d"),d=-1!==this.options.template.indexOf("DD"),e=31;if(this.options.smartDays&&this.$month&&this.$year){var f=parseInt(this.$month.val(),10),g=parseInt(this.$year.val(),10);isNaN(f)||isNaN(g)||(e=moment([g,f]).daysInMonth())}for(b=1;e>=b;b++)a=d?this.leadZero(b):b,c.push([b,a]);return c},fillMonth:function(){var a,b,c=this.fillCommon("M"),d=-1!==this.options.template.indexOf("MMMM"),e=-1!==this.options.template.indexOf("MMM"),f=-1!==this.options.template.indexOf("MM");for(b=0;11>=b;b++)a=d?moment().date(1).month(b).format("MMMM"):e?moment().date(1).month(b).format("MMM"):f?this.leadZero(b+1):b+1,c.push([b,a]);return c},fillYear:function(){var a,b,c=[],d=-1!==this.options.template.indexOf("YYYY");for(b=this.options.maxYear;b>=this.options.minYear;b--)a=d?b:(b+"").substring(2),c[this.options.yearDescending?"push":"unshift"]([b,a]);return c=this.fillCommon("y").concat(c)},fillHour:function(){var a,b,c=this.fillCommon("h"),d=-1!==this.options.template.indexOf("h"),e=(-1!==this.options.template.indexOf("H"),-1!==this.options.template.toLowerCase().indexOf("hh")),f=d?1:0,g=d?12:23;for(b=f;g>=b;b++)a=e?this.leadZero(b):b,c.push([b,a]);return c},fillMinute:function(){var a,b,c=this.fillCommon("m"),d=-1!==this.options.template.indexOf("mm");for(b=0;59>=b;b+=this.options.minuteStep)a=d?this.leadZero(b):b,c.push([b,a]);return c},fillSecond:function(){var a,b,c=this.fillCommon("s"),d=-1!==this.options.template.indexOf("ss");for(b=0;59>=b;b+=this.options.secondStep)a=d?this.leadZero(b):b,c.push([b,a]);return c},fillAmpm:function(){var a=-1!==this.options.template.indexOf("a"),b=(-1!==this.options.template.indexOf("A"),[["am",a?"am":"AM"],["pm",a?"pm":"PM"]]);return b},getValue:function(a){var b,c={},d=this,e=!1;return angular.forEach(this.map,function(a,b){if("ampm"!==b){var f="day"===b?1:0;return c[b]=d["$"+b]?parseInt(d["$"+b].val(),10):f,isNaN(c[b])?(e=!0,!1):void 0}}),e?"":(this.$ampm&&(12===c.hour?c.hour="am"===this.$ampm.val()?0:12:c.hour="am"===this.$ampm.val()?c.hour:c.hour+12),b=moment([c.year,c.month,c.day,c.hour,c.minute,c.second]),this.highlight(b),a=void 0===a?this.options.format:a,null===a?b.isValid()?b:null:b.isValid()?b.format(a):"")},setValue:function(a){function b(a,b){var c={};return angular.forEach(a.children("option"),function(a,d){var e=angular.element(a).attr("value");if(""!==e){var f=Math.abs(e-b);("undefined"==typeof c.distance||f<c.distance)&&(c={value:e,distance:f})}}),c.value}if(a){var c="string"==typeof a?moment(a,this.options.format,!0):moment(a),d=this,e={};c.isValid()&&(angular.forEach(this.map,function(a,b){"ampm"!==b&&(e[b]=c[a[1]]())}),this.$ampm&&(e.hour>=12?(e.ampm="pm",e.hour>12&&(e.hour-=12)):(e.ampm="am",0===e.hour&&(e.hour=12))),angular.forEach(e,function(a,c){d["$"+c]&&("minute"===c&&d.options.minuteStep>1&&d.options.roundTime&&(a=b(d["$"+c],a)),"second"===c&&d.options.secondStep>1&&d.options.roundTime&&(a=b(d["$"+c],a)),d["$"+c].val(a))}),this.options.smartDays&&this.fillCombo("day"),this.$element.val(c.format(this.options.format)).triggerHandler("change"))}},highlight:function(a){a.isValid()?this.options.errorClass?this.$widget.removeClass(this.options.errorClass):this.$widget.find("select").css("border-color",this.borderColor):this.options.errorClass?this.$widget.addClass(this.options.errorClass):(this.borderColor||(this.borderColor=this.$widget.find("select").css("border-color")),this.$widget.find("select").css("border-color","red"))},leadZero:function(a){return 9>=a?"0"+a:a},destroy:function(){this.$widget.remove(),this.$element.removeData("combodate").show()}},{getInstance:function(b,c){return new a(b,c)}}}]),angular.module("xeditable").factory("editableIcons",function(){var a={"default":{bs2:{ok:"icon-ok icon-white",cancel:"icon-remove"},bs3:{ok:"glyphicon glyphicon-ok",cancel:"glyphicon glyphicon-remove"}},external:{"font-awesome":{ok:"fa fa-check",cancel:"fa fa-times"}}};return a}),angular.module("xeditable").factory("editableThemes",function(){var a={"default":{formTpl:'<form class="editable-wrap"></form>',noformTpl:'<span class="editable-wrap"></span>',controlsTpl:'<span class="editable-controls"></span>',inputTpl:"",errorTpl:'<div class="editable-error" ng-show="$error" ng-bind="$error"></div>',buttonsTpl:'<span class="editable-buttons"></span>',submitTpl:'<button type="submit">save</button>',cancelTpl:'<button type="button" ng-click="$form.$cancel()">cancel</button>'},bs2:{formTpl:'<form class="form-inline editable-wrap" role="form"></form>',noformTpl:'<span class="editable-wrap"></span>',controlsTpl:'<div class="editable-controls controls control-group" ng-class="{\'error\': $error}"></div>',inputTpl:"",errorTpl:'<div class="editable-error help-block" ng-show="$error" ng-bind="$error"></div>',buttonsTpl:'<span class="editable-buttons"></span>',submitTpl:'<button type="submit" class="btn btn-primary"><span></span></button>',cancelTpl:'<button type="button" class="btn" ng-click="$form.$cancel()"><span></span></button>'},bs3:{formTpl:'<form class="form-inline editable-wrap" role="form"></form>',noformTpl:'<span class="editable-wrap"></span>',controlsTpl:'<div class="editable-controls form-group" ng-class="{\'has-error\': $error}"></div>',inputTpl:"",errorTpl:'<div class="editable-error help-block" ng-show="$error" ng-bind="$error"></div>',buttonsTpl:'<span class="editable-buttons"></span>',submitTpl:'<button type="submit" class="btn btn-primary"><span></span></button>',cancelTpl:'<button type="button" class="btn btn-default" ng-click="$form.$cancel()"><span></span></button>',buttonsClass:"",inputClass:"",postrender:function(){switch(this.directiveName){case"editableText":case"editableSelect":case"editableTextarea":case"editableEmail":case"editableTel":case"editableNumber":case"editableUrl":case"editableSearch":case"editableDate":case"editableDatetime":case"editableBsdate":case"editableTime":case"editableMonth":case"editableWeek":case"editablePassword":if(this.inputEl.addClass("form-control"),this.theme.inputClass){if(this.inputEl.attr("multiple")&&("input-sm"===this.theme.inputClass||"input-lg"===this.theme.inputClass))break;this.inputEl.addClass(this.theme.inputClass)}break;case"editableCheckbox":this.editorEl.addClass("checkbox")}this.buttonsEl&&this.theme.buttonsClass&&this.buttonsEl.find("button").addClass(this.theme.buttonsClass)}},semantic:{formTpl:'<form class="editable-wrap ui form" ng-class="{\'error\': $error}" role="form"></form>',noformTpl:'<span class="editable-wrap"></span>',controlsTpl:'<div class="editable-controls ui fluid input" ng-class="{\'error\': $error}"></div>',inputTpl:"",errorTpl:'<div class="editable-error ui error message" ng-show="$error" ng-bind="$error"></div>',buttonsTpl:'<span class="mini ui buttons"></span>',submitTpl:'<button type="submit" class="ui primary button"><i class="ui check icon"></i></button>',cancelTpl:'<button type="button" class="ui button" ng-click="$form.$cancel()"><i class="ui cancel icon"></i></button>'}};return a});;/**!
 * AngularJS file upload directives and services. Supoorts: file upload/drop/paste, resume, cancel/abort,
 * progress, resize, thumbnail, preview, validation and CORS
 * @author  Danial  <danial.farid@gmail.com>
 * @version 12.2.13
 */

if (window.XMLHttpRequest && !(window.FileAPI && FileAPI.shouldLoad)) {
  window.XMLHttpRequest.prototype.setRequestHeader = (function (orig) {
    return function (header, value) {
      if (header === '__setXHR_') {
        var val = value(this);
        // fix for angular < 1.2.0
        if (val instanceof Function) {
          val(this);
        }
      } else {
        orig.apply(this, arguments);
      }
    };
  })(window.XMLHttpRequest.prototype.setRequestHeader);
}

var ngFileUpload = angular.module('ngFileUpload', []);

ngFileUpload.version = '12.2.13';

ngFileUpload.service('UploadBase', ['$http', '$q', '$timeout', function ($http, $q, $timeout) {
  var upload = this;
  upload.promisesCount = 0;

  this.isResumeSupported = function () {
    return window.Blob && window.Blob.prototype.slice;
  };

  var resumeSupported = this.isResumeSupported();

  function sendHttp(config) {
    config.method = config.method || 'POST';
    config.headers = config.headers || {};

    var deferred = config._deferred = config._deferred || $q.defer();
    var promise = deferred.promise;

    function notifyProgress(e) {
      if (deferred.notify) {
        deferred.notify(e);
      }
      if (promise.progressFunc) {
        $timeout(function () {
          promise.progressFunc(e);
        });
      }
    }

    function getNotifyEvent(n) {
      if (config._start != null && resumeSupported) {
        return {
          loaded: n.loaded + config._start,
          total: (config._file && config._file.size) || n.total,
          type: n.type, config: config,
          lengthComputable: true, target: n.target
        };
      } else {
        return n;
      }
    }

    if (!config.disableProgress) {
      config.headers.__setXHR_ = function () {
        return function (xhr) {
          if (!xhr || !xhr.upload || !xhr.upload.addEventListener) return;
          config.__XHR = xhr;
          if (config.xhrFn) config.xhrFn(xhr);
          xhr.upload.addEventListener('progress', function (e) {
            e.config = config;
            notifyProgress(getNotifyEvent(e));
          }, false);
          //fix for firefox not firing upload progress end, also IE8-9
          xhr.upload.addEventListener('load', function (e) {
            if (e.lengthComputable) {
              e.config = config;
              notifyProgress(getNotifyEvent(e));
            }
          }, false);
        };
      };
    }

    function uploadWithAngular() {
      $http(config).then(function (r) {
          if (resumeSupported && config._chunkSize && !config._finished && config._file) {
            var fileSize = config._file && config._file.size || 0;
            notifyProgress({
                loaded: Math.min(config._end, fileSize),
                total: fileSize,
                config: config,
                type: 'progress'
              }
            );
            upload.upload(config, true);
          } else {
            if (config._finished) delete config._finished;
            deferred.resolve(r);
          }
        }, function (e) {
          deferred.reject(e);
        }, function (n) {
          deferred.notify(n);
        }
      );
    }

    if (!resumeSupported) {
      uploadWithAngular();
    } else if (config._chunkSize && config._end && !config._finished) {
      config._start = config._end;
      config._end += config._chunkSize;
      uploadWithAngular();
    } else if (config.resumeSizeUrl) {
      $http.get(config.resumeSizeUrl).then(function (resp) {
        if (config.resumeSizeResponseReader) {
          config._start = config.resumeSizeResponseReader(resp.data);
        } else {
          config._start = parseInt((resp.data.size == null ? resp.data : resp.data.size).toString());
        }
        if (config._chunkSize) {
          config._end = config._start + config._chunkSize;
        }
        uploadWithAngular();
      }, function (e) {
        throw e;
      });
    } else if (config.resumeSize) {
      config.resumeSize().then(function (size) {
        config._start = size;
        if (config._chunkSize) {
          config._end = config._start + config._chunkSize;
        }
        uploadWithAngular();
      }, function (e) {
        throw e;
      });
    } else {
      if (config._chunkSize) {
        config._start = 0;
        config._end = config._start + config._chunkSize;
      }
      uploadWithAngular();
    }


    promise.success = function (fn) {
      promise.then(function (response) {
        fn(response.data, response.status, response.headers, config);
      });
      return promise;
    };

    promise.error = function (fn) {
      promise.then(null, function (response) {
        fn(response.data, response.status, response.headers, config);
      });
      return promise;
    };

    promise.progress = function (fn) {
      promise.progressFunc = fn;
      promise.then(null, null, function (n) {
        fn(n);
      });
      return promise;
    };
    promise.abort = promise.pause = function () {
      if (config.__XHR) {
        $timeout(function () {
          config.__XHR.abort();
        });
      }
      return promise;
    };
    promise.xhr = function (fn) {
      config.xhrFn = (function (origXhrFn) {
        return function () {
          if (origXhrFn) origXhrFn.apply(promise, arguments);
          fn.apply(promise, arguments);
        };
      })(config.xhrFn);
      return promise;
    };

    upload.promisesCount++;
    if (promise['finally'] && promise['finally'] instanceof Function) {
      promise['finally'](function () {
        upload.promisesCount--;
      });
    }
    return promise;
  }

  this.isUploadInProgress = function () {
    return upload.promisesCount > 0;
  };

  this.rename = function (file, name) {
    file.ngfName = name;
    return file;
  };

  this.jsonBlob = function (val) {
    if (val != null && !angular.isString(val)) {
      val = JSON.stringify(val);
    }
    var blob = new window.Blob([val], {type: 'application/json'});
    blob._ngfBlob = true;
    return blob;
  };

  this.json = function (val) {
    return angular.toJson(val);
  };

  function copy(obj) {
    var clone = {};
    for (var key in obj) {
      if (obj.hasOwnProperty(key)) {
        clone[key] = obj[key];
      }
    }
    return clone;
  }

  this.isFile = function (file) {
    return file != null && (file instanceof window.Blob || (file.flashId && file.name && file.size));
  };

  this.upload = function (config, internal) {
    function toResumeFile(file, formData) {
      if (file._ngfBlob) return file;
      config._file = config._file || file;
      if (config._start != null && resumeSupported) {
        if (config._end && config._end >= file.size) {
          config._finished = true;
          config._end = file.size;
        }
        var slice = file.slice(config._start, config._end || file.size);
        slice.name = file.name;
        slice.ngfName = file.ngfName;
        if (config._chunkSize) {
          formData.append('_chunkSize', config._chunkSize);
          formData.append('_currentChunkSize', config._end - config._start);
          formData.append('_chunkNumber', Math.floor(config._start / config._chunkSize));
          formData.append('_totalSize', config._file.size);
        }
        return slice;
      }
      return file;
    }

    function addFieldToFormData(formData, val, key) {
      if (val !== undefined) {
        if (angular.isDate(val)) {
          val = val.toISOString();
        }
        if (angular.isString(val)) {
          formData.append(key, val);
        } else if (upload.isFile(val)) {
          var file = toResumeFile(val, formData);
          var split = key.split(',');
          if (split[1]) {
            file.ngfName = split[1].replace(/^\s+|\s+$/g, '');
            key = split[0];
          }
          config._fileKey = config._fileKey || key;
          formData.append(key, file, file.ngfName || file.name);
        } else {
          if (angular.isObject(val)) {
            if (val.$$ngfCircularDetection) throw 'ngFileUpload: Circular reference in config.data. Make sure specified data for Upload.upload() has no circular reference: ' + key;

            val.$$ngfCircularDetection = true;
            try {
              for (var k in val) {
                if (val.hasOwnProperty(k) && k !== '$$ngfCircularDetection') {
                  var objectKey = config.objectKey == null ? '[i]' : config.objectKey;
                  if (val.length && parseInt(k) > -1) {
                    objectKey = config.arrayKey == null ? objectKey : config.arrayKey;
                  }
                  addFieldToFormData(formData, val[k], key + objectKey.replace(/[ik]/g, k));
                }
              }
            } finally {
              delete val.$$ngfCircularDetection;
            }
          } else {
            formData.append(key, val);
          }
        }
      }
    }

    function digestConfig() {
      config._chunkSize = upload.translateScalars(config.resumeChunkSize);
      config._chunkSize = config._chunkSize ? parseInt(config._chunkSize.toString()) : null;

      config.headers = config.headers || {};
      config.headers['Content-Type'] = undefined;
      config.transformRequest = config.transformRequest ?
        (angular.isArray(config.transformRequest) ?
          config.transformRequest : [config.transformRequest]) : [];
      config.transformRequest.push(function (data) {
        var formData = new window.FormData(), key;
        data = data || config.fields || {};
        if (config.file) {
          data.file = config.file;
        }
        for (key in data) {
          if (data.hasOwnProperty(key)) {
            var val = data[key];
            if (config.formDataAppender) {
              config.formDataAppender(formData, key, val);
            } else {
              addFieldToFormData(formData, val, key);
            }
          }
        }

        return formData;
      });
    }

    if (!internal) config = copy(config);
    if (!config._isDigested) {
      config._isDigested = true;
      digestConfig();
    }

    return sendHttp(config);
  };

  this.http = function (config) {
    config = copy(config);
    config.transformRequest = config.transformRequest || function (data) {
        if ((window.ArrayBuffer && data instanceof window.ArrayBuffer) || data instanceof window.Blob) {
          return data;
        }
        return $http.defaults.transformRequest[0].apply(this, arguments);
      };
    config._chunkSize = upload.translateScalars(config.resumeChunkSize);
    config._chunkSize = config._chunkSize ? parseInt(config._chunkSize.toString()) : null;

    return sendHttp(config);
  };

  this.translateScalars = function (str) {
    if (angular.isString(str)) {
      if (str.search(/kb/i) === str.length - 2) {
        return parseFloat(str.substring(0, str.length - 2) * 1024);
      } else if (str.search(/mb/i) === str.length - 2) {
        return parseFloat(str.substring(0, str.length - 2) * 1048576);
      } else if (str.search(/gb/i) === str.length - 2) {
        return parseFloat(str.substring(0, str.length - 2) * 1073741824);
      } else if (str.search(/b/i) === str.length - 1) {
        return parseFloat(str.substring(0, str.length - 1));
      } else if (str.search(/s/i) === str.length - 1) {
        return parseFloat(str.substring(0, str.length - 1));
      } else if (str.search(/m/i) === str.length - 1) {
        return parseFloat(str.substring(0, str.length - 1) * 60);
      } else if (str.search(/h/i) === str.length - 1) {
        return parseFloat(str.substring(0, str.length - 1) * 3600);
      }
    }
    return str;
  };

  this.urlToBlob = function(url) {
    var defer = $q.defer();
    $http({url: url, method: 'get', responseType: 'arraybuffer'}).then(function (resp) {
      var arrayBufferView = new Uint8Array(resp.data);
      var type = resp.headers('content-type') || 'image/WebP';
      var blob = new window.Blob([arrayBufferView], {type: type});
      var matches = url.match(/.*\/(.+?)(\?.*)?$/);
      if (matches.length > 1) {
        blob.name = matches[1];
      }
      defer.resolve(blob);
    }, function (e) {
      defer.reject(e);
    });
    return defer.promise;
  };

  this.setDefaults = function (defaults) {
    this.defaults = defaults || {};
  };

  this.defaults = {};
  this.version = ngFileUpload.version;
}

]);

ngFileUpload.service('Upload', ['$parse', '$timeout', '$compile', '$q', 'UploadExif', function ($parse, $timeout, $compile, $q, UploadExif) {
  var upload = UploadExif;
  upload.getAttrWithDefaults = function (attr, name) {
    if (attr[name] != null) return attr[name];
    var def = upload.defaults[name];
    return (def == null ? def : (angular.isString(def) ? def : JSON.stringify(def)));
  };

  upload.attrGetter = function (name, attr, scope, params) {
    var attrVal = this.getAttrWithDefaults(attr, name);
    if (scope) {
      try {
        if (params) {
          return $parse(attrVal)(scope, params);
        } else {
          return $parse(attrVal)(scope);
        }
      } catch (e) {
        // hangle string value without single qoute
        if (name.search(/min|max|pattern/i)) {
          return attrVal;
        } else {
          throw e;
        }
      }
    } else {
      return attrVal;
    }
  };

  upload.shouldUpdateOn = function (type, attr, scope) {
    var modelOptions = upload.attrGetter('ngfModelOptions', attr, scope);
    if (modelOptions && modelOptions.updateOn) {
      return modelOptions.updateOn.split(' ').indexOf(type) > -1;
    }
    return true;
  };

  upload.emptyPromise = function () {
    var d = $q.defer();
    var args = arguments;
    $timeout(function () {
      d.resolve.apply(d, args);
    });
    return d.promise;
  };

  upload.rejectPromise = function () {
    var d = $q.defer();
    var args = arguments;
    $timeout(function () {
      d.reject.apply(d, args);
    });
    return d.promise;
  };

  upload.happyPromise = function (promise, data) {
    var d = $q.defer();
    promise.then(function (result) {
      d.resolve(result);
    }, function (error) {
      $timeout(function () {
        throw error;
      });
      d.resolve(data);
    });
    return d.promise;
  };

  function applyExifRotations(files, attr, scope) {
    var promises = [upload.emptyPromise()];
    angular.forEach(files, function (f, i) {
      if (f.type.indexOf('image/jpeg') === 0 && upload.attrGetter('ngfFixOrientation', attr, scope, {$file: f})) {
        promises.push(upload.happyPromise(upload.applyExifRotation(f), f).then(function (fixedFile) {
          files.splice(i, 1, fixedFile);
        }));
      }
    });
    return $q.all(promises);
  }

  function resizeFile(files, attr, scope, ngModel) {
    var resizeVal = upload.attrGetter('ngfResize', attr, scope);
    if (!resizeVal || !upload.isResizeSupported() || !files.length) return upload.emptyPromise();
    if (resizeVal instanceof Function) {
      var defer = $q.defer();
      return resizeVal(files).then(function (p) {
        resizeWithParams(p, files, attr, scope, ngModel).then(function (r) {
          defer.resolve(r);
        }, function (e) {
          defer.reject(e);
        });
      }, function (e) {
        defer.reject(e);
      });
    } else {
      return resizeWithParams(resizeVal, files, attr, scope, ngModel);
    }
  }

  function resizeWithParams(params, files, attr, scope, ngModel) {
    var promises = [upload.emptyPromise()];

    function handleFile(f, i) {
      if (f.type.indexOf('image') === 0) {
        if (params.pattern && !upload.validatePattern(f, params.pattern)) return;
        params.resizeIf = function (width, height) {
          return upload.attrGetter('ngfResizeIf', attr, scope,
            {$width: width, $height: height, $file: f});
        };
        var promise = upload.resize(f, params);
        promises.push(promise);
        promise.then(function (resizedFile) {
          files.splice(i, 1, resizedFile);
        }, function (e) {
          f.$error = 'resize';
          (f.$errorMessages = (f.$errorMessages || {})).resize = true;
          f.$errorParam = (e ? (e.message ? e.message : e) + ': ' : '') + (f && f.name);
          ngModel.$ngfValidations.push({name: 'resize', valid: false});
          upload.applyModelValidation(ngModel, files);
        });
      }
    }

    for (var i = 0; i < files.length; i++) {
      handleFile(files[i], i);
    }
    return $q.all(promises);
  }

  upload.updateModel = function (ngModel, attr, scope, fileChange, files, evt, noDelay) {
    function update(files, invalidFiles, newFiles, dupFiles, isSingleModel) {
      attr.$$ngfPrevValidFiles = files;
      attr.$$ngfPrevInvalidFiles = invalidFiles;
      var file = files && files.length ? files[0] : null;
      var invalidFile = invalidFiles && invalidFiles.length ? invalidFiles[0] : null;

      if (ngModel) {
        upload.applyModelValidation(ngModel, files);
        ngModel.$setViewValue(isSingleModel ? file : files);
      }

      if (fileChange) {
        $parse(fileChange)(scope, {
          $files: files,
          $file: file,
          $newFiles: newFiles,
          $duplicateFiles: dupFiles,
          $invalidFiles: invalidFiles,
          $invalidFile: invalidFile,
          $event: evt
        });
      }

      var invalidModel = upload.attrGetter('ngfModelInvalid', attr);
      if (invalidModel) {
        $timeout(function () {
          $parse(invalidModel).assign(scope, isSingleModel ? invalidFile : invalidFiles);
        });
      }
      $timeout(function () {
        // scope apply changes
      });
    }

    var allNewFiles, dupFiles = [], prevValidFiles, prevInvalidFiles,
      invalids = [], valids = [];

    function removeDuplicates() {
      function equals(f1, f2) {
        return f1.name === f2.name && (f1.$ngfOrigSize || f1.size) === (f2.$ngfOrigSize || f2.size) &&
          f1.type === f2.type;
      }

      function isInPrevFiles(f) {
        var j;
        for (j = 0; j < prevValidFiles.length; j++) {
          if (equals(f, prevValidFiles[j])) {
            return true;
          }
        }
        for (j = 0; j < prevInvalidFiles.length; j++) {
          if (equals(f, prevInvalidFiles[j])) {
            return true;
          }
        }
        return false;
      }

      if (files) {
        allNewFiles = [];
        dupFiles = [];
        for (var i = 0; i < files.length; i++) {
          if (isInPrevFiles(files[i])) {
            dupFiles.push(files[i]);
          } else {
            allNewFiles.push(files[i]);
          }
        }
      }
    }

    function toArray(v) {
      return angular.isArray(v) ? v : [v];
    }

    function resizeAndUpdate() {
      function updateModel() {
        $timeout(function () {
          update(keep ? prevValidFiles.concat(valids) : valids,
            keep ? prevInvalidFiles.concat(invalids) : invalids,
            files, dupFiles, isSingleModel);
        }, options && options.debounce ? options.debounce.change || options.debounce : 0);
      }

      var resizingFiles = validateAfterResize ? allNewFiles : valids;
      resizeFile(resizingFiles, attr, scope, ngModel).then(function () {
        if (validateAfterResize) {
          upload.validate(allNewFiles, keep ? prevValidFiles.length : 0, ngModel, attr, scope)
            .then(function (validationResult) {
              valids = validationResult.validsFiles;
              invalids = validationResult.invalidsFiles;
              updateModel();
            });
        } else {
          updateModel();
        }
      }, function () {
        for (var i = 0; i < resizingFiles.length; i++) {
          var f = resizingFiles[i];
          if (f.$error === 'resize') {
            var index = valids.indexOf(f);
            if (index > -1) {
              valids.splice(index, 1);
              invalids.push(f);
            }
            updateModel();
          }
        }
      });
    }

    prevValidFiles = attr.$$ngfPrevValidFiles || [];
    prevInvalidFiles = attr.$$ngfPrevInvalidFiles || [];
    if (ngModel && ngModel.$modelValue) {
      prevValidFiles = toArray(ngModel.$modelValue);
    }

    var keep = upload.attrGetter('ngfKeep', attr, scope);
    allNewFiles = (files || []).slice(0);
    if (keep === 'distinct' || upload.attrGetter('ngfKeepDistinct', attr, scope) === true) {
      removeDuplicates(attr, scope);
    }

    var isSingleModel = !keep && !upload.attrGetter('ngfMultiple', attr, scope) && !upload.attrGetter('multiple', attr);

    if (keep && !allNewFiles.length) return;

    upload.attrGetter('ngfBeforeModelChange', attr, scope, {
      $files: files,
      $file: files && files.length ? files[0] : null,
      $newFiles: allNewFiles,
      $duplicateFiles: dupFiles,
      $event: evt
    });

    var validateAfterResize = upload.attrGetter('ngfValidateAfterResize', attr, scope);

    var options = upload.attrGetter('ngfModelOptions', attr, scope);
    upload.validate(allNewFiles, keep ? prevValidFiles.length : 0, ngModel, attr, scope)
      .then(function (validationResult) {
      if (noDelay) {
        update(allNewFiles, [], files, dupFiles, isSingleModel);
      } else {
        if ((!options || !options.allowInvalid) && !validateAfterResize) {
          valids = validationResult.validFiles;
          invalids = validationResult.invalidFiles;
        } else {
          valids = allNewFiles;
        }
        if (upload.attrGetter('ngfFixOrientation', attr, scope) && upload.isExifSupported()) {
          applyExifRotations(valids, attr, scope).then(function () {
            resizeAndUpdate();
          });
        } else {
          resizeAndUpdate();
        }
      }
    });
  };

  return upload;
}]);

ngFileUpload.directive('ngfSelect', ['$parse', '$timeout', '$compile', 'Upload', function ($parse, $timeout, $compile, Upload) {
  var generatedElems = [];

  function isDelayedClickSupported(ua) {
    // fix for android native browser < 4.4 and safari windows
    var m = ua.match(/Android[^\d]*(\d+)\.(\d+)/);
    if (m && m.length > 2) {
      var v = Upload.defaults.androidFixMinorVersion || 4;
      return parseInt(m[1]) < 4 || (parseInt(m[1]) === v && parseInt(m[2]) < v);
    }

    // safari on windows
    return ua.indexOf('Chrome') === -1 && /.*Windows.*Safari.*/.test(ua);
  }

  function linkFileSelect(scope, elem, attr, ngModel, $parse, $timeout, $compile, upload) {
    /** @namespace attr.ngfSelect */
    /** @namespace attr.ngfChange */
    /** @namespace attr.ngModel */
    /** @namespace attr.ngfModelOptions */
    /** @namespace attr.ngfMultiple */
    /** @namespace attr.ngfCapture */
    /** @namespace attr.ngfValidate */
    /** @namespace attr.ngfKeep */
    var attrGetter = function (name, scope) {
      return upload.attrGetter(name, attr, scope);
    };

    function isInputTypeFile() {
      return elem[0].tagName.toLowerCase() === 'input' && attr.type && attr.type.toLowerCase() === 'file';
    }

    function fileChangeAttr() {
      return attrGetter('ngfChange') || attrGetter('ngfSelect');
    }

    function changeFn(evt) {
      if (upload.shouldUpdateOn('change', attr, scope)) {
        var fileList = evt.__files_ || (evt.target && evt.target.files), files = [];
        /* Handle duplicate call in  IE11 */
        if (!fileList) return;
        for (var i = 0; i < fileList.length; i++) {
          files.push(fileList[i]);
        }
        upload.updateModel(ngModel, attr, scope, fileChangeAttr(),
          files.length ? files : null, evt);
      }
    }

    upload.registerModelChangeValidator(ngModel, attr, scope);

    var unwatches = [];
    if (attrGetter('ngfMultiple')) {
      unwatches.push(scope.$watch(attrGetter('ngfMultiple'), function () {
        fileElem.attr('multiple', attrGetter('ngfMultiple', scope));
      }));
    }
    if (attrGetter('ngfCapture')) {
      unwatches.push(scope.$watch(attrGetter('ngfCapture'), function () {
        fileElem.attr('capture', attrGetter('ngfCapture', scope));
      }));
    }
    if (attrGetter('ngfAccept')) {
      unwatches.push(scope.$watch(attrGetter('ngfAccept'), function () {
        fileElem.attr('accept', attrGetter('ngfAccept', scope));
      }));
    }
    unwatches.push(attr.$observe('accept', function () {
      fileElem.attr('accept', attrGetter('accept'));
    }));
    function bindAttrToFileInput(fileElem, label) {
      function updateId(val) {
        fileElem.attr('id', 'ngf-' + val);
        label.attr('id', 'ngf-label-' + val);
      }

      for (var i = 0; i < elem[0].attributes.length; i++) {
        var attribute = elem[0].attributes[i];
        if (attribute.name !== 'type' && attribute.name !== 'class' && attribute.name !== 'style') {
          if (attribute.name === 'id') {
            updateId(attribute.value);
            unwatches.push(attr.$observe('id', updateId));
          } else {
            fileElem.attr(attribute.name, (!attribute.value && (attribute.name === 'required' ||
            attribute.name === 'multiple')) ? attribute.name : attribute.value);
          }
        }
      }
    }

    function createFileInput() {
      if (isInputTypeFile()) {
        return elem;
      }

      var fileElem = angular.element('<input type="file">');

      var label = angular.element('<label>upload</label>');
      label.css('visibility', 'hidden').css('position', 'absolute').css('overflow', 'hidden')
        .css('width', '0px').css('height', '0px').css('border', 'none')
        .css('margin', '0px').css('padding', '0px').attr('tabindex', '-1');
      bindAttrToFileInput(fileElem, label);

      generatedElems.push({el: elem, ref: label});

      document.body.appendChild(label.append(fileElem)[0]);

      return fileElem;
    }

    function clickHandler(evt) {
      if (elem.attr('disabled')) return false;
      if (attrGetter('ngfSelectDisabled', scope)) return;

      var r = detectSwipe(evt);
      // prevent the click if it is a swipe
      if (r != null) return r;

      resetModel(evt);

      // fix for md when the element is removed from the DOM and added back #460
      try {
        if (!isInputTypeFile() && !document.body.contains(fileElem[0])) {
          generatedElems.push({el: elem, ref: fileElem.parent()});
          document.body.appendChild(fileElem.parent()[0]);
          fileElem.bind('change', changeFn);
        }
      } catch (e) {/*ignore*/
      }

      if (isDelayedClickSupported(navigator.userAgent)) {
        setTimeout(function () {
          fileElem[0].click();
        }, 0);
      } else {
        fileElem[0].click();
      }

      return false;
    }


    var initialTouchStartY = 0;
    var initialTouchStartX = 0;

    function detectSwipe(evt) {
      var touches = evt.changedTouches || (evt.originalEvent && evt.originalEvent.changedTouches);
      if (touches) {
        if (evt.type === 'touchstart') {
          initialTouchStartX = touches[0].clientX;
          initialTouchStartY = touches[0].clientY;
          return true; // don't block event default
        } else {
          // prevent scroll from triggering event
          if (evt.type === 'touchend') {
            var currentX = touches[0].clientX;
            var currentY = touches[0].clientY;
            if ((Math.abs(currentX - initialTouchStartX) > 20) ||
              (Math.abs(currentY - initialTouchStartY) > 20)) {
              evt.stopPropagation();
              evt.preventDefault();
              return false;
            }
          }
          return true;
        }
      }
    }

    var fileElem = elem;

    function resetModel(evt) {
      if (upload.shouldUpdateOn('click', attr, scope) && fileElem.val()) {
        fileElem.val(null);
        upload.updateModel(ngModel, attr, scope, fileChangeAttr(), null, evt, true);
      }
    }

    if (!isInputTypeFile()) {
      fileElem = createFileInput();
    }
    fileElem.bind('change', changeFn);

    if (!isInputTypeFile()) {
      elem.bind('click touchstart touchend', clickHandler);
    } else {
      elem.bind('click', resetModel);
    }

    function ie10SameFileSelectFix(evt) {
      if (fileElem && !fileElem.attr('__ngf_ie10_Fix_')) {
        if (!fileElem[0].parentNode) {
          fileElem = null;
          return;
        }
        evt.preventDefault();
        evt.stopPropagation();
        fileElem.unbind('click');
        var clone = fileElem.clone();
        fileElem.replaceWith(clone);
        fileElem = clone;
        fileElem.attr('__ngf_ie10_Fix_', 'true');
        fileElem.bind('change', changeFn);
        fileElem.bind('click', ie10SameFileSelectFix);
        fileElem[0].click();
        return false;
      } else {
        fileElem.removeAttr('__ngf_ie10_Fix_');
      }
    }

    if (navigator.appVersion.indexOf('MSIE 10') !== -1) {
      fileElem.bind('click', ie10SameFileSelectFix);
    }

    if (ngModel) ngModel.$formatters.push(function (val) {
      if (val == null || val.length === 0) {
        if (fileElem.val()) {
          fileElem.val(null);
        }
      }
      return val;
    });

    scope.$on('$destroy', function () {
      if (!isInputTypeFile()) fileElem.parent().remove();
      angular.forEach(unwatches, function (unwatch) {
        unwatch();
      });
    });

    $timeout(function () {
      for (var i = 0; i < generatedElems.length; i++) {
        var g = generatedElems[i];
        if (!document.body.contains(g.el[0])) {
          generatedElems.splice(i, 1);
          g.ref.remove();
        }
      }
    });

    if (window.FileAPI && window.FileAPI.ngfFixIE) {
      window.FileAPI.ngfFixIE(elem, fileElem, changeFn);
    }
  }

  return {
    restrict: 'AEC',
    require: '?ngModel',
    link: function (scope, elem, attr, ngModel) {
      linkFileSelect(scope, elem, attr, ngModel, $parse, $timeout, $compile, Upload);
    }
  };
}]);

(function () {

  ngFileUpload.service('UploadDataUrl', ['UploadBase', '$timeout', '$q', function (UploadBase, $timeout, $q) {
    var upload = UploadBase;
    upload.base64DataUrl = function (file) {
      if (angular.isArray(file)) {
        var d = $q.defer(), count = 0;
        angular.forEach(file, function (f) {
          upload.dataUrl(f, true)['finally'](function () {
            count++;
            if (count === file.length) {
              var urls = [];
              angular.forEach(file, function (ff) {
                urls.push(ff.$ngfDataUrl);
              });
              d.resolve(urls, file);
            }
          });
        });
        return d.promise;
      } else {
        return upload.dataUrl(file, true);
      }
    };
    upload.dataUrl = function (file, disallowObjectUrl) {
      if (!file) return upload.emptyPromise(file, file);
      if ((disallowObjectUrl && file.$ngfDataUrl != null) || (!disallowObjectUrl && file.$ngfBlobUrl != null)) {
        return upload.emptyPromise(disallowObjectUrl ? file.$ngfDataUrl : file.$ngfBlobUrl, file);
      }
      var p = disallowObjectUrl ? file.$$ngfDataUrlPromise : file.$$ngfBlobUrlPromise;
      if (p) return p;

      var deferred = $q.defer();
      $timeout(function () {
        if (window.FileReader && file &&
          (!window.FileAPI || navigator.userAgent.indexOf('MSIE 8') === -1 || file.size < 20000) &&
          (!window.FileAPI || navigator.userAgent.indexOf('MSIE 9') === -1 || file.size < 4000000)) {
          //prefer URL.createObjectURL for handling refrences to files of all sizes
          //since it doesn´t build a large string in memory
          var URL = window.URL || window.webkitURL;
          if (URL && URL.createObjectURL && !disallowObjectUrl) {
            var url;
            try {
              url = URL.createObjectURL(file);
            } catch (e) {
              $timeout(function () {
                file.$ngfBlobUrl = '';
                deferred.reject();
              });
              return;
            }
            $timeout(function () {
              file.$ngfBlobUrl = url;
              if (url) {
                deferred.resolve(url, file);
                upload.blobUrls = upload.blobUrls || [];
                upload.blobUrlsTotalSize = upload.blobUrlsTotalSize || 0;
                upload.blobUrls.push({url: url, size: file.size});
                upload.blobUrlsTotalSize += file.size || 0;
                var maxMemory = upload.defaults.blobUrlsMaxMemory || 268435456;
                var maxLength = upload.defaults.blobUrlsMaxQueueSize || 200;
                while ((upload.blobUrlsTotalSize > maxMemory || upload.blobUrls.length > maxLength) && upload.blobUrls.length > 1) {
                  var obj = upload.blobUrls.splice(0, 1)[0];
                  URL.revokeObjectURL(obj.url);
                  upload.blobUrlsTotalSize -= obj.size;
                }
              }
            });
          } else {
            var fileReader = new FileReader();
            fileReader.onload = function (e) {
              $timeout(function () {
                file.$ngfDataUrl = e.target.result;
                deferred.resolve(e.target.result, file);
                $timeout(function () {
                  delete file.$ngfDataUrl;
                }, 1000);
              });
            };
            fileReader.onerror = function () {
              $timeout(function () {
                file.$ngfDataUrl = '';
                deferred.reject();
              });
            };
            fileReader.readAsDataURL(file);
          }
        } else {
          $timeout(function () {
            file[disallowObjectUrl ? '$ngfDataUrl' : '$ngfBlobUrl'] = '';
            deferred.reject();
          });
        }
      });

      if (disallowObjectUrl) {
        p = file.$$ngfDataUrlPromise = deferred.promise;
      } else {
        p = file.$$ngfBlobUrlPromise = deferred.promise;
      }
      p['finally'](function () {
        delete file[disallowObjectUrl ? '$$ngfDataUrlPromise' : '$$ngfBlobUrlPromise'];
      });
      return p;
    };
    return upload;
  }]);

  function getTagType(el) {
    if (el.tagName.toLowerCase() === 'img') return 'image';
    if (el.tagName.toLowerCase() === 'audio') return 'audio';
    if (el.tagName.toLowerCase() === 'video') return 'video';
    return /./;
  }

  function linkFileDirective(Upload, $timeout, scope, elem, attr, directiveName, resizeParams, isBackground) {
    function constructDataUrl(file) {
      var disallowObjectUrl = Upload.attrGetter('ngfNoObjectUrl', attr, scope);
      Upload.dataUrl(file, disallowObjectUrl)['finally'](function () {
        $timeout(function () {
          var src = (disallowObjectUrl ? file.$ngfDataUrl : file.$ngfBlobUrl) || file.$ngfDataUrl;
          if (isBackground) {
            elem.css('background-image', 'url(\'' + (src || '') + '\')');
          } else {
            elem.attr('src', src);
          }
          if (src) {
            elem.removeClass('ng-hide');
          } else {
            elem.addClass('ng-hide');
          }
        });
      });
    }

    $timeout(function () {
      var unwatch = scope.$watch(attr[directiveName], function (file) {
        var size = resizeParams;
        if (directiveName === 'ngfThumbnail') {
          if (!size) {
            size = {
              width: elem[0].naturalWidth || elem[0].clientWidth,
              height: elem[0].naturalHeight || elem[0].clientHeight
            };
          }
          if (size.width === 0 && window.getComputedStyle) {
            var style = getComputedStyle(elem[0]);
            if (style.width && style.width.indexOf('px') > -1 && style.height && style.height.indexOf('px') > -1) {
              size = {
                width: parseInt(style.width.slice(0, -2)),
                height: parseInt(style.height.slice(0, -2))
              };
            }
          }
        }

        if (angular.isString(file)) {
          elem.removeClass('ng-hide');
          if (isBackground) {
            return elem.css('background-image', 'url(\'' + file + '\')');
          } else {
            return elem.attr('src', file);
          }
        }
        if (file && file.type && file.type.search(getTagType(elem[0])) === 0 &&
          (!isBackground || file.type.indexOf('image') === 0)) {
          if (size && Upload.isResizeSupported()) {
            size.resizeIf = function (width, height) {
              return Upload.attrGetter('ngfResizeIf', attr, scope,
                {$width: width, $height: height, $file: file});
            };
            Upload.resize(file, size).then(
              function (f) {
                constructDataUrl(f);
              }, function (e) {
                throw e;
              }
            );
          } else {
            constructDataUrl(file);
          }
        } else {
          elem.addClass('ng-hide');
        }
      });

      scope.$on('$destroy', function () {
        unwatch();
      });
    });
  }


  /** @namespace attr.ngfSrc */
  /** @namespace attr.ngfNoObjectUrl */
  ngFileUpload.directive('ngfSrc', ['Upload', '$timeout', function (Upload, $timeout) {
    return {
      restrict: 'AE',
      link: function (scope, elem, attr) {
        linkFileDirective(Upload, $timeout, scope, elem, attr, 'ngfSrc',
          Upload.attrGetter('ngfResize', attr, scope), false);
      }
    };
  }]);

  /** @namespace attr.ngfBackground */
  /** @namespace attr.ngfNoObjectUrl */
  ngFileUpload.directive('ngfBackground', ['Upload', '$timeout', function (Upload, $timeout) {
    return {
      restrict: 'AE',
      link: function (scope, elem, attr) {
        linkFileDirective(Upload, $timeout, scope, elem, attr, 'ngfBackground',
          Upload.attrGetter('ngfResize', attr, scope), true);
      }
    };
  }]);

  /** @namespace attr.ngfThumbnail */
  /** @namespace attr.ngfAsBackground */
  /** @namespace attr.ngfSize */
  /** @namespace attr.ngfNoObjectUrl */
  ngFileUpload.directive('ngfThumbnail', ['Upload', '$timeout', function (Upload, $timeout) {
    return {
      restrict: 'AE',
      link: function (scope, elem, attr) {
        var size = Upload.attrGetter('ngfSize', attr, scope);
        linkFileDirective(Upload, $timeout, scope, elem, attr, 'ngfThumbnail', size,
          Upload.attrGetter('ngfAsBackground', attr, scope));
      }
    };
  }]);

  ngFileUpload.config(['$compileProvider', function ($compileProvider) {
    if ($compileProvider.imgSrcSanitizationWhitelist) $compileProvider.imgSrcSanitizationWhitelist(/^\s*(https?|ftp|mailto|tel|webcal|local|file|data|blob):/);
    if ($compileProvider.aHrefSanitizationWhitelist) $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|mailto|tel|webcal|local|file|data|blob):/);
  }]);

  ngFileUpload.filter('ngfDataUrl', ['UploadDataUrl', '$sce', function (UploadDataUrl, $sce) {
    return function (file, disallowObjectUrl, trustedUrl) {
      if (angular.isString(file)) {
        return $sce.trustAsResourceUrl(file);
      }
      var src = file && ((disallowObjectUrl ? file.$ngfDataUrl : file.$ngfBlobUrl) || file.$ngfDataUrl);
      if (file && !src) {
        if (!file.$ngfDataUrlFilterInProgress && angular.isObject(file)) {
          file.$ngfDataUrlFilterInProgress = true;
          UploadDataUrl.dataUrl(file, disallowObjectUrl);
        }
        return '';
      }
      if (file) delete file.$ngfDataUrlFilterInProgress;
      return (file && src ? (trustedUrl ? $sce.trustAsResourceUrl(src) : src) : file) || '';
    };
  }]);

})();

ngFileUpload.service('UploadValidate', ['UploadDataUrl', '$q', '$timeout', function (UploadDataUrl, $q, $timeout) {
  var upload = UploadDataUrl;

  function globStringToRegex(str) {
    var regexp = '', excludes = [];
    if (str.length > 2 && str[0] === '/' && str[str.length - 1] === '/') {
      regexp = str.substring(1, str.length - 1);
    } else {
      var split = str.split(',');
      if (split.length > 1) {
        for (var i = 0; i < split.length; i++) {
          var r = globStringToRegex(split[i]);
          if (r.regexp) {
            regexp += '(' + r.regexp + ')';
            if (i < split.length - 1) {
              regexp += '|';
            }
          } else {
            excludes = excludes.concat(r.excludes);
          }
        }
      } else {
        if (str.indexOf('!') === 0) {
          excludes.push('^((?!' + globStringToRegex(str.substring(1)).regexp + ').)*$');
        } else {
          if (str.indexOf('.') === 0) {
            str = '*' + str;
          }
          regexp = '^' + str.replace(new RegExp('[.\\\\+*?\\[\\^\\]$(){}=!<>|:\\-]', 'g'), '\\$&') + '$';
          regexp = regexp.replace(/\\\*/g, '.*').replace(/\\\?/g, '.');
        }
      }
    }
    return {regexp: regexp, excludes: excludes};
  }

  upload.validatePattern = function (file, val) {
    if (!val) {
      return true;
    }
    var pattern = globStringToRegex(val), valid = true;
    if (pattern.regexp && pattern.regexp.length) {
      var regexp = new RegExp(pattern.regexp, 'i');
      valid = (file.type != null && regexp.test(file.type)) ||
        (file.name != null && regexp.test(file.name));
    }
    var len = pattern.excludes.length;
    while (len--) {
      var exclude = new RegExp(pattern.excludes[len], 'i');
      valid = valid && (file.type == null || exclude.test(file.type)) &&
        (file.name == null || exclude.test(file.name));
    }
    return valid;
  };

  upload.ratioToFloat = function (val) {
    var r = val.toString(), xIndex = r.search(/[x:]/i);
    if (xIndex > -1) {
      r = parseFloat(r.substring(0, xIndex)) / parseFloat(r.substring(xIndex + 1));
    } else {
      r = parseFloat(r);
    }
    return r;
  };

  upload.registerModelChangeValidator = function (ngModel, attr, scope) {
    if (ngModel) {
      ngModel.$formatters.push(function (files) {
        if (ngModel.$dirty) {
          var filesArray = files;
          if (files && !angular.isArray(files)) {
            filesArray = [files];
          }
          upload.validate(filesArray, 0, ngModel, attr, scope).then(function () {
            upload.applyModelValidation(ngModel, filesArray);
          });
        }
        return files;
      });
    }
  };

  function markModelAsDirty(ngModel, files) {
    if (files != null && !ngModel.$dirty) {
      if (ngModel.$setDirty) {
        ngModel.$setDirty();
      } else {
        ngModel.$dirty = true;
      }
    }
  }

  upload.applyModelValidation = function (ngModel, files) {
    markModelAsDirty(ngModel, files);
    angular.forEach(ngModel.$ngfValidations, function (validation) {
      ngModel.$setValidity(validation.name, validation.valid);
    });
  };

  upload.getValidationAttr = function (attr, scope, name, validationName, file) {
    var dName = 'ngf' + name[0].toUpperCase() + name.substr(1);
    var val = upload.attrGetter(dName, attr, scope, {$file: file});
    if (val == null) {
      val = upload.attrGetter('ngfValidate', attr, scope, {$file: file});
      if (val) {
        var split = (validationName || name).split('.');
        val = val[split[0]];
        if (split.length > 1) {
          val = val && val[split[1]];
        }
      }
    }
    return val;
  };

  upload.validate = function (files, prevLength, ngModel, attr, scope) {
    ngModel = ngModel || {};
    ngModel.$ngfValidations = ngModel.$ngfValidations || [];

    angular.forEach(ngModel.$ngfValidations, function (v) {
      v.valid = true;
    });

    var attrGetter = function (name, params) {
      return upload.attrGetter(name, attr, scope, params);
    };

    var ignoredErrors = (upload.attrGetter('ngfIgnoreInvalid', attr, scope) || '').split(' ');
    var runAllValidation = upload.attrGetter('ngfRunAllValidations', attr, scope);

    if (files == null || files.length === 0) {
      return upload.emptyPromise({'validFiles': files, 'invalidFiles': []});
    }

    files = files.length === undefined ? [files] : files.slice(0);
    var invalidFiles = [];

    function validateSync(name, validationName, fn) {
      if (files) {
        var i = files.length, valid = null;
        while (i--) {
          var file = files[i];
          if (file) {
            var val = upload.getValidationAttr(attr, scope, name, validationName, file);
            if (val != null) {
              if (!fn(file, val, i)) {
                if (ignoredErrors.indexOf(name) === -1) {
                  file.$error = name;
                  (file.$errorMessages = (file.$errorMessages || {}))[name] = true;
                  file.$errorParam = val;
                  if (invalidFiles.indexOf(file) === -1) {
                    invalidFiles.push(file);
                  }
                  if (!runAllValidation) {
                    files.splice(i, 1);
                  }
                  valid = false;
                } else {
                  files.splice(i, 1);
                }
              }
            }
          }
        }
        if (valid !== null) {
          ngModel.$ngfValidations.push({name: name, valid: valid});
        }
      }
    }

    validateSync('pattern', null, upload.validatePattern);
    validateSync('minSize', 'size.min', function (file, val) {
      return file.size + 0.1 >= upload.translateScalars(val);
    });
    validateSync('maxSize', 'size.max', function (file, val) {
      return file.size - 0.1 <= upload.translateScalars(val);
    });
    var totalSize = 0;
    validateSync('maxTotalSize', null, function (file, val) {
      totalSize += file.size;
      if (totalSize > upload.translateScalars(val)) {
        files.splice(0, files.length);
        return false;
      }
      return true;
    });

    validateSync('validateFn', null, function (file, r) {
      return r === true || r === null || r === '';
    });

    if (!files.length) {
      return upload.emptyPromise({'validFiles': [], 'invalidFiles': invalidFiles});
    }

    function validateAsync(name, validationName, type, asyncFn, fn) {
      function resolveResult(defer, file, val) {
        function resolveInternal(fn) {
          if (fn()) {
            if (ignoredErrors.indexOf(name) === -1) {
              file.$error = name;
              (file.$errorMessages = (file.$errorMessages || {}))[name] = true;
              file.$errorParam = val;
              if (invalidFiles.indexOf(file) === -1) {
                invalidFiles.push(file);
              }
              if (!runAllValidation) {
                var i = files.indexOf(file);
                if (i > -1) files.splice(i, 1);
              }
              defer.resolve(false);
            } else {
              var j = files.indexOf(file);
              if (j > -1) files.splice(j, 1);
              defer.resolve(true);
            }
          } else {
            defer.resolve(true);
          }
        }

        if (val != null) {
          asyncFn(file, val).then(function (d) {
            resolveInternal(function () {
              return !fn(d, val);
            });
          }, function () {
            resolveInternal(function () {
              return attrGetter('ngfValidateForce', {$file: file});
            });
          });
        } else {
          defer.resolve(true);
        }
      }

      var promises = [upload.emptyPromise(true)];
      if (files) {
        files = files.length === undefined ? [files] : files;
        angular.forEach(files, function (file) {
          var defer = $q.defer();
          promises.push(defer.promise);
          if (type && (file.type == null || file.type.search(type) !== 0)) {
            defer.resolve(true);
            return;
          }
          if (name === 'dimensions' && upload.attrGetter('ngfDimensions', attr) != null) {
            upload.imageDimensions(file).then(function (d) {
              resolveResult(defer, file,
                attrGetter('ngfDimensions', {$file: file, $width: d.width, $height: d.height}));
            }, function () {
              defer.resolve(false);
            });
          } else if (name === 'duration' && upload.attrGetter('ngfDuration', attr) != null) {
            upload.mediaDuration(file).then(function (d) {
              resolveResult(defer, file,
                attrGetter('ngfDuration', {$file: file, $duration: d}));
            }, function () {
              defer.resolve(false);
            });
          } else {
            resolveResult(defer, file,
              upload.getValidationAttr(attr, scope, name, validationName, file));
          }
        });
      }
      var deffer = $q.defer();
      $q.all(promises).then(function (values) {
        var isValid = true;
        for (var i = 0; i < values.length; i++) {
          if (!values[i]) {
            isValid = false;
            break;
          }
        }
        ngModel.$ngfValidations.push({name: name, valid: isValid});
        deffer.resolve(isValid);
      });
      return deffer.promise;
    }

    var deffer = $q.defer();
    var promises = [];

    promises.push(validateAsync('maxHeight', 'height.max', /image/,
      this.imageDimensions, function (d, val) {
        return d.height <= val;
      }));
    promises.push(validateAsync('minHeight', 'height.min', /image/,
      this.imageDimensions, function (d, val) {
        return d.height >= val;
      }));
    promises.push(validateAsync('maxWidth', 'width.max', /image/,
      this.imageDimensions, function (d, val) {
        return d.width <= val;
      }));
    promises.push(validateAsync('minWidth', 'width.min', /image/,
      this.imageDimensions, function (d, val) {
        return d.width >= val;
      }));
    promises.push(validateAsync('dimensions', null, /image/,
      function (file, val) {
        return upload.emptyPromise(val);
      }, function (r) {
        return r;
      }));
    promises.push(validateAsync('ratio', null, /image/,
      this.imageDimensions, function (d, val) {
        var split = val.toString().split(','), valid = false;
        for (var i = 0; i < split.length; i++) {
          if (Math.abs((d.width / d.height) - upload.ratioToFloat(split[i])) < 0.01) {
            valid = true;
          }
        }
        return valid;
      }));
    promises.push(validateAsync('maxRatio', 'ratio.max', /image/,
      this.imageDimensions, function (d, val) {
        return (d.width / d.height) - upload.ratioToFloat(val) < 0.0001;
      }));
    promises.push(validateAsync('minRatio', 'ratio.min', /image/,
      this.imageDimensions, function (d, val) {
        return (d.width / d.height) - upload.ratioToFloat(val) > -0.0001;
      }));
    promises.push(validateAsync('maxDuration', 'duration.max', /audio|video/,
      this.mediaDuration, function (d, val) {
        return d <= upload.translateScalars(val);
      }));
    promises.push(validateAsync('minDuration', 'duration.min', /audio|video/,
      this.mediaDuration, function (d, val) {
        return d >= upload.translateScalars(val);
      }));
    promises.push(validateAsync('duration', null, /audio|video/,
      function (file, val) {
        return upload.emptyPromise(val);
      }, function (r) {
        return r;
      }));

    promises.push(validateAsync('validateAsyncFn', null, null,
      function (file, val) {
        return val;
      }, function (r) {
        return r === true || r === null || r === '';
      }));

    $q.all(promises).then(function () {

      if (runAllValidation) {
        for (var i = 0; i < files.length; i++) {
          var file = files[i];
          if (file.$error) {
            files.splice(i--, 1);
          }
        }
      }

      runAllValidation = false;
      validateSync('maxFiles', null, function (file, val, i) {
        return prevLength + i < val;
      });

      deffer.resolve({'validFiles': files, 'invalidFiles': invalidFiles});
    });
    return deffer.promise;
  };

  upload.imageDimensions = function (file) {
    if (file.$ngfWidth && file.$ngfHeight) {
      var d = $q.defer();
      $timeout(function () {
        d.resolve({width: file.$ngfWidth, height: file.$ngfHeight});
      });
      return d.promise;
    }
    if (file.$ngfDimensionPromise) return file.$ngfDimensionPromise;

    var deferred = $q.defer();
    $timeout(function () {
      if (file.type.indexOf('image') !== 0) {
        deferred.reject('not image');
        return;
      }
      upload.dataUrl(file).then(function (dataUrl) {
        var img = angular.element('<img>').attr('src', dataUrl)
          .css('visibility', 'hidden').css('position', 'fixed')
          .css('max-width', 'none !important').css('max-height', 'none !important');

        function success() {
          var width = img[0].naturalWidth || img[0].clientWidth;
          var height = img[0].naturalHeight || img[0].clientHeight;
          img.remove();
          file.$ngfWidth = width;
          file.$ngfHeight = height;
          deferred.resolve({width: width, height: height});
        }

        function error() {
          img.remove();
          deferred.reject('load error');
        }

        img.on('load', success);
        img.on('error', error);

        var secondsCounter = 0;
        function checkLoadErrorInCaseOfNoCallback() {
          $timeout(function () {
            if (img[0].parentNode) {
              if (img[0].clientWidth) {
                success();
              } else if (secondsCounter++ > 10) {
                error();
              } else {
                checkLoadErrorInCaseOfNoCallback();
              }
            }
          }, 1000);
        }

        checkLoadErrorInCaseOfNoCallback();

        angular.element(document.getElementsByTagName('body')[0]).append(img);
      }, function () {
        deferred.reject('load error');
      });
    });

    file.$ngfDimensionPromise = deferred.promise;
    file.$ngfDimensionPromise['finally'](function () {
      delete file.$ngfDimensionPromise;
    });
    return file.$ngfDimensionPromise;
  };

  upload.mediaDuration = function (file) {
    if (file.$ngfDuration) {
      var d = $q.defer();
      $timeout(function () {
        d.resolve(file.$ngfDuration);
      });
      return d.promise;
    }
    if (file.$ngfDurationPromise) return file.$ngfDurationPromise;

    var deferred = $q.defer();
    $timeout(function () {
      if (file.type.indexOf('audio') !== 0 && file.type.indexOf('video') !== 0) {
        deferred.reject('not media');
        return;
      }
      upload.dataUrl(file).then(function (dataUrl) {
        var el = angular.element(file.type.indexOf('audio') === 0 ? '<audio>' : '<video>')
          .attr('src', dataUrl).css('visibility', 'none').css('position', 'fixed');

        function success() {
          var duration = el[0].duration;
          file.$ngfDuration = duration;
          el.remove();
          deferred.resolve(duration);
        }

        function error() {
          el.remove();
          deferred.reject('load error');
        }

        el.on('loadedmetadata', success);
        el.on('error', error);
        var count = 0;

        function checkLoadError() {
          $timeout(function () {
            if (el[0].parentNode) {
              if (el[0].duration) {
                success();
              } else if (count > 10) {
                error();
              } else {
                checkLoadError();
              }
            }
          }, 1000);
        }

        checkLoadError();

        angular.element(document.body).append(el);
      }, function () {
        deferred.reject('load error');
      });
    });

    file.$ngfDurationPromise = deferred.promise;
    file.$ngfDurationPromise['finally'](function () {
      delete file.$ngfDurationPromise;
    });
    return file.$ngfDurationPromise;
  };
  return upload;
}
]);

ngFileUpload.service('UploadResize', ['UploadValidate', '$q', function (UploadValidate, $q) {
  var upload = UploadValidate;

  /**
   * Conserve aspect ratio of the original region. Useful when shrinking/enlarging
   * images to fit into a certain area.
   * Source:  http://stackoverflow.com/a/14731922
   *
   * @param {Number} srcWidth Source area width
   * @param {Number} srcHeight Source area height
   * @param {Number} maxWidth Nestable area maximum available width
   * @param {Number} maxHeight Nestable area maximum available height
   * @return {Object} { width, height }
   */
  var calculateAspectRatioFit = function (srcWidth, srcHeight, maxWidth, maxHeight, centerCrop) {
    var ratio = centerCrop ? Math.max(maxWidth / srcWidth, maxHeight / srcHeight) :
      Math.min(maxWidth / srcWidth, maxHeight / srcHeight);
    return {
      width: srcWidth * ratio, height: srcHeight * ratio,
      marginX: srcWidth * ratio - maxWidth, marginY: srcHeight * ratio - maxHeight
    };
  };

  // Extracted from https://github.com/romelgomez/angular-firebase-image-upload/blob/master/app/scripts/fileUpload.js#L89
  var resize = function (imagen, width, height, quality, type, ratio, centerCrop, resizeIf) {
    var deferred = $q.defer();
    var canvasElement = document.createElement('canvas');
    var imageElement = document.createElement('img');
    imageElement.setAttribute('style', 'visibility:hidden;position:fixed;z-index:-100000');
    document.body.appendChild(imageElement);

    imageElement.onload = function () {
      var imgWidth = imageElement.width, imgHeight = imageElement.height;
      imageElement.parentNode.removeChild(imageElement);
      if (resizeIf != null && resizeIf(imgWidth, imgHeight) === false) {
        deferred.reject('resizeIf');
        return;
      }
      try {
        if (ratio) {
          var ratioFloat = upload.ratioToFloat(ratio);
          var imgRatio = imgWidth / imgHeight;
          if (imgRatio < ratioFloat) {
            width = imgWidth;
            height = width / ratioFloat;
          } else {
            height = imgHeight;
            width = height * ratioFloat;
          }
        }
        if (!width) {
          width = imgWidth;
        }
        if (!height) {
          height = imgHeight;
        }
        var dimensions = calculateAspectRatioFit(imgWidth, imgHeight, width, height, centerCrop);
        canvasElement.width = Math.min(dimensions.width, width);
        canvasElement.height = Math.min(dimensions.height, height);
        var context = canvasElement.getContext('2d');
        context.drawImage(imageElement,
          Math.min(0, -dimensions.marginX / 2), Math.min(0, -dimensions.marginY / 2),
          dimensions.width, dimensions.height);
        deferred.resolve(canvasElement.toDataURL(type || 'image/WebP', quality || 0.934));
      } catch (e) {
        deferred.reject(e);
      }
    };
    imageElement.onerror = function () {
      imageElement.parentNode.removeChild(imageElement);
      deferred.reject();
    };
    imageElement.src = imagen;
    return deferred.promise;
  };

  upload.dataUrltoBlob = function (dataurl, name, origSize) {
    var arr = dataurl.split(','), mime = arr[0].match(/:(.*?);/)[1],
      bstr = atob(arr[1]), n = bstr.length, u8arr = new Uint8Array(n);
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    var blob = new window.Blob([u8arr], {type: mime});
    blob.name = name;
    blob.$ngfOrigSize = origSize;
    return blob;
  };

  upload.isResizeSupported = function () {
    var elem = document.createElement('canvas');
    return window.atob && elem.getContext && elem.getContext('2d') && window.Blob;
  };

  if (upload.isResizeSupported()) {
    // add name getter to the blob constructor prototype
    Object.defineProperty(window.Blob.prototype, 'name', {
      get: function () {
        return this.$ngfName;
      },
      set: function (v) {
        this.$ngfName = v;
      },
      configurable: true
    });
  }

  upload.resize = function (file, options) {
    if (file.type.indexOf('image') !== 0) return upload.emptyPromise(file);

    var deferred = $q.defer();
    upload.dataUrl(file, true).then(function (url) {
      resize(url, options.width, options.height, options.quality, options.type || file.type,
        options.ratio, options.centerCrop, options.resizeIf)
        .then(function (dataUrl) {
          if (file.type === 'image/jpeg' && options.restoreExif !== false) {
            try {
              dataUrl = upload.restoreExif(url, dataUrl);
            } catch (e) {
              setTimeout(function () {throw e;}, 1);
            }
          }
          try {
            var blob = upload.dataUrltoBlob(dataUrl, file.name, file.size);
            deferred.resolve(blob);
          } catch (e) {
            deferred.reject(e);
          }
        }, function (r) {
          if (r === 'resizeIf') {
            deferred.resolve(file);
          }
          deferred.reject(r);
        });
    }, function (e) {
      deferred.reject(e);
    });
    return deferred.promise;
  };

  return upload;
}]);

(function () {
  ngFileUpload.directive('ngfDrop', ['$parse', '$timeout', '$window', 'Upload', '$http', '$q',
    function ($parse, $timeout, $window, Upload, $http, $q) {
      return {
        restrict: 'AEC',
        require: '?ngModel',
        link: function (scope, elem, attr, ngModel) {
          linkDrop(scope, elem, attr, ngModel, $parse, $timeout, $window, Upload, $http, $q);
        }
      };
    }]);

  ngFileUpload.directive('ngfNoFileDrop', function () {
    return function (scope, elem) {
      if (dropAvailable()) elem.css('display', 'none');
    };
  });

  ngFileUpload.directive('ngfDropAvailable', ['$parse', '$timeout', 'Upload', function ($parse, $timeout, Upload) {
    return function (scope, elem, attr) {
      if (dropAvailable()) {
        var model = $parse(Upload.attrGetter('ngfDropAvailable', attr));
        $timeout(function () {
          model(scope);
          if (model.assign) {
            model.assign(scope, true);
          }
        });
      }
    };
  }]);

  function linkDrop(scope, elem, attr, ngModel, $parse, $timeout, $window, upload, $http, $q) {
    var available = dropAvailable();

    var attrGetter = function (name, scope, params) {
      return upload.attrGetter(name, attr, scope, params);
    };

    if (attrGetter('dropAvailable')) {
      $timeout(function () {
        if (scope[attrGetter('dropAvailable')]) {
          scope[attrGetter('dropAvailable')].value = available;
        } else {
          scope[attrGetter('dropAvailable')] = available;
        }
      });
    }
    if (!available) {
      if (attrGetter('ngfHideOnDropNotAvailable', scope) === true) {
        elem.css('display', 'none');
      }
      return;
    }

    function isDisabled() {
      return elem.attr('disabled') || attrGetter('ngfDropDisabled', scope);
    }

    if (attrGetter('ngfSelect') == null) {
      upload.registerModelChangeValidator(ngModel, attr, scope);
    }

    var leaveTimeout = null;
    var stopPropagation = $parse(attrGetter('ngfStopPropagation'));
    var dragOverDelay = 1;
    var actualDragOverClass;

    elem[0].addEventListener('dragover', function (evt) {
      if (isDisabled() || !upload.shouldUpdateOn('drop', attr, scope)) return;
      evt.preventDefault();
      if (stopPropagation(scope)) evt.stopPropagation();
      // handling dragover events from the Chrome download bar
      if (navigator.userAgent.indexOf('Chrome') > -1) {
        var b = evt.dataTransfer.effectAllowed;
        evt.dataTransfer.dropEffect = ('move' === b || 'linkMove' === b) ? 'move' : 'copy';
      }
      $timeout.cancel(leaveTimeout);
      if (!actualDragOverClass) {
        actualDragOverClass = 'C';
        calculateDragOverClass(scope, attr, evt, function (clazz) {
          actualDragOverClass = clazz;
          elem.addClass(actualDragOverClass);
          attrGetter('ngfDrag', scope, {$isDragging: true, $class: actualDragOverClass, $event: evt});
        });
      }
    }, false);
    elem[0].addEventListener('dragenter', function (evt) {
      if (isDisabled() || !upload.shouldUpdateOn('drop', attr, scope)) return;
      evt.preventDefault();
      if (stopPropagation(scope)) evt.stopPropagation();
    }, false);
    elem[0].addEventListener('dragleave', function (evt) {
      if (isDisabled() || !upload.shouldUpdateOn('drop', attr, scope)) return;
      evt.preventDefault();
      if (stopPropagation(scope)) evt.stopPropagation();
      leaveTimeout = $timeout(function () {
        if (actualDragOverClass) elem.removeClass(actualDragOverClass);
        actualDragOverClass = null;
        attrGetter('ngfDrag', scope, {$isDragging: false, $event: evt});
      }, dragOverDelay || 100);
    }, false);
    elem[0].addEventListener('drop', function (evt) {
      if (isDisabled() || !upload.shouldUpdateOn('drop', attr, scope)) return;
      evt.preventDefault();
      if (stopPropagation(scope)) evt.stopPropagation();
      if (actualDragOverClass) elem.removeClass(actualDragOverClass);
      actualDragOverClass = null;
      extractFilesAndUpdateModel(evt.dataTransfer, evt, 'dropUrl');
    }, false);
    elem[0].addEventListener('paste', function (evt) {
      if (navigator.userAgent.toLowerCase().indexOf('firefox') > -1 &&
        attrGetter('ngfEnableFirefoxPaste', scope)) {
        evt.preventDefault();
      }
      if (isDisabled() || !upload.shouldUpdateOn('paste', attr, scope)) return;
      extractFilesAndUpdateModel(evt.clipboardData || evt.originalEvent.clipboardData, evt, 'pasteUrl');
    }, false);

    if (navigator.userAgent.toLowerCase().indexOf('firefox') > -1 &&
      attrGetter('ngfEnableFirefoxPaste', scope)) {
      elem.attr('contenteditable', true);
      elem.on('keypress', function (e) {
        if (!e.metaKey && !e.ctrlKey) {
          e.preventDefault();
        }
      });
    }

    function extractFilesAndUpdateModel(source, evt, updateOnType) {
      if (!source) return;
      // html needs to be calculated on the same process otherwise the data will be wiped
      // after promise resolve or setTimeout.
      var html;
      try {
        html = source && source.getData && source.getData('text/html');
      } catch (e) {/* Fix IE11 that throw error calling getData */
      }
      extractFiles(source.items, source.files, attrGetter('ngfAllowDir', scope) !== false,
        attrGetter('multiple') || attrGetter('ngfMultiple', scope)).then(function (files) {
        if (files.length) {
          updateModel(files, evt);
        } else {
          extractFilesFromHtml(updateOnType, html).then(function (files) {
            updateModel(files, evt);
          });
        }
      });
    }

    function updateModel(files, evt) {
      upload.updateModel(ngModel, attr, scope, attrGetter('ngfChange') || attrGetter('ngfDrop'), files, evt);
    }

    function extractFilesFromHtml(updateOn, html) {
      if (!upload.shouldUpdateOn(updateOn, attr, scope) || typeof html !== 'string') return upload.rejectPromise([]);
      var urls = [];
      html.replace(/<(img src|img [^>]* src) *=\"([^\"]*)\"/gi, function (m, n, src) {
        urls.push(src);
      });
      var promises = [], files = [];
      if (urls.length) {
        angular.forEach(urls, function (url) {
          promises.push(upload.urlToBlob(url).then(function (blob) {
            files.push(blob);
          }));
        });
        var defer = $q.defer();
        $q.all(promises).then(function () {
          defer.resolve(files);
        }, function (e) {
          defer.reject(e);
        });
        return defer.promise;
      }
      return upload.emptyPromise();
    }

    function calculateDragOverClass(scope, attr, evt, callback) {
      var obj = attrGetter('ngfDragOverClass', scope, {$event: evt}), dClass = 'dragover';
      if (angular.isString(obj)) {
        dClass = obj;
      } else if (obj) {
        if (obj.delay) dragOverDelay = obj.delay;
        if (obj.accept || obj.reject) {
          var items = evt.dataTransfer.items;
          if (items == null || !items.length) {
            dClass = obj.accept;
          } else {
            var pattern = obj.pattern || attrGetter('ngfPattern', scope, {$event: evt});
            var len = items.length;
            while (len--) {
              if (!upload.validatePattern(items[len], pattern)) {
                dClass = obj.reject;
                break;
              } else {
                dClass = obj.accept;
              }
            }
          }
        }
      }
      callback(dClass);
    }

    function extractFiles(items, fileList, allowDir, multiple) {
      var maxFiles = upload.getValidationAttr(attr, scope, 'maxFiles');
      if (maxFiles == null) {
        maxFiles = Number.MAX_VALUE;
      }
      var maxTotalSize = upload.getValidationAttr(attr, scope, 'maxTotalSize');
      if (maxTotalSize == null) {
        maxTotalSize = Number.MAX_VALUE;
      }
      var includeDir = attrGetter('ngfIncludeDir', scope);
      var files = [], totalSize = 0;

      function traverseFileTree(entry, path) {
        var defer = $q.defer();
        if (entry != null) {
          if (entry.isDirectory) {
            var promises = [upload.emptyPromise()];
            if (includeDir) {
              var file = {type: 'directory'};
              file.name = file.path = (path || '') + entry.name;
              files.push(file);
            }
            var dirReader = entry.createReader();
            var entries = [];
            var readEntries = function () {
              dirReader.readEntries(function (results) {
                try {
                  if (!results.length) {
                    angular.forEach(entries.slice(0), function (e) {
                      if (files.length <= maxFiles && totalSize <= maxTotalSize) {
                        promises.push(traverseFileTree(e, (path ? path : '') + entry.name + '/'));
                      }
                    });
                    $q.all(promises).then(function () {
                      defer.resolve();
                    }, function (e) {
                      defer.reject(e);
                    });
                  } else {
                    entries = entries.concat(Array.prototype.slice.call(results || [], 0));
                    readEntries();
                  }
                } catch (e) {
                  defer.reject(e);
                }
              }, function (e) {
                defer.reject(e);
              });
            };
            readEntries();
          } else {
            entry.file(function (file) {
              try {
                file.path = (path ? path : '') + file.name;
                if (includeDir) {
                  file = upload.rename(file, file.path);
                }
                files.push(file);
                totalSize += file.size;
                defer.resolve();
              } catch (e) {
                defer.reject(e);
              }
            }, function (e) {
              defer.reject(e);
            });
          }
        }
        return defer.promise;
      }

      var promises = [upload.emptyPromise()];

      if (items && items.length > 0 && $window.location.protocol !== 'file:') {
        for (var i = 0; i < items.length; i++) {
          if (items[i].webkitGetAsEntry && items[i].webkitGetAsEntry() && items[i].webkitGetAsEntry().isDirectory) {
            var entry = items[i].webkitGetAsEntry();
            if (entry.isDirectory && !allowDir) {
              continue;
            }
            if (entry != null) {
              promises.push(traverseFileTree(entry));
            }
          } else {
            var f = items[i].getAsFile();
            if (f != null) {
              files.push(f);
              totalSize += f.size;
            }
          }
          if (files.length > maxFiles || totalSize > maxTotalSize ||
            (!multiple && files.length > 0)) break;
        }
      } else {
        if (fileList != null) {
          for (var j = 0; j < fileList.length; j++) {
            var file = fileList.item(j);
            if (file.type || file.size > 0) {
              files.push(file);
              totalSize += file.size;
            }
            if (files.length > maxFiles || totalSize > maxTotalSize ||
              (!multiple && files.length > 0)) break;
          }
        }
      }

      var defer = $q.defer();
      $q.all(promises).then(function () {
        if (!multiple && !includeDir && files.length) {
          var i = 0;
          while (files[i] && files[i].type === 'directory') i++;
          defer.resolve([files[i]]);
        } else {
          defer.resolve(files);
        }
      }, function (e) {
        defer.reject(e);
      });

      return defer.promise;
    }
  }

  function dropAvailable() {
    var div = document.createElement('div');
    return ('draggable' in div) && ('ondrop' in div) && !/Edge\/12./i.test(navigator.userAgent);
  }

})();

// customized version of https://github.com/exif-js/exif-js
ngFileUpload.service('UploadExif', ['UploadResize', '$q', function (UploadResize, $q) {
  var upload = UploadResize;

  upload.isExifSupported = function () {
    return window.FileReader && new FileReader().readAsArrayBuffer && upload.isResizeSupported();
  };

  function applyTransform(ctx, orientation, width, height) {
    switch (orientation) {
      case 2:
        return ctx.transform(-1, 0, 0, 1, width, 0);
      case 3:
        return ctx.transform(-1, 0, 0, -1, width, height);
      case 4:
        return ctx.transform(1, 0, 0, -1, 0, height);
      case 5:
        return ctx.transform(0, 1, 1, 0, 0, 0);
      case 6:
        return ctx.transform(0, 1, -1, 0, height, 0);
      case 7:
        return ctx.transform(0, -1, -1, 0, height, width);
      case 8:
        return ctx.transform(0, -1, 1, 0, 0, width);
    }
  }

  upload.readOrientation = function (file) {
    var defer = $q.defer();
    var reader = new FileReader();
    var slicedFile = file.slice ? file.slice(0, 64 * 1024) : file;
    reader.readAsArrayBuffer(slicedFile);
    reader.onerror = function (e) {
      return defer.reject(e);
    };
    reader.onload = function (e) {
      var result = {orientation: 1};
      var view = new DataView(this.result);
      if (view.getUint16(0, false) !== 0xFFD8) return defer.resolve(result);

      var length = view.byteLength,
        offset = 2;
      while (offset < length) {
        var marker = view.getUint16(offset, false);
        offset += 2;
        if (marker === 0xFFE1) {
          if (view.getUint32(offset += 2, false) !== 0x45786966) return defer.resolve(result);

          var little = view.getUint16(offset += 6, false) === 0x4949;
          offset += view.getUint32(offset + 4, little);
          var tags = view.getUint16(offset, little);
          offset += 2;
          for (var i = 0; i < tags; i++)
            if (view.getUint16(offset + (i * 12), little) === 0x0112) {
              var orientation = view.getUint16(offset + (i * 12) + 8, little);
              if (orientation >= 2 && orientation <= 8) {
                view.setUint16(offset + (i * 12) + 8, 1, little);
                result.fixedArrayBuffer = e.target.result;
              }
              result.orientation = orientation;
              return defer.resolve(result);
            }
        } else if ((marker & 0xFF00) !== 0xFF00) break;
        else offset += view.getUint16(offset, false);
      }
      return defer.resolve(result);
    };
    return defer.promise;
  };

  function arrayBufferToBase64(buffer) {
    var binary = '';
    var bytes = new Uint8Array(buffer);
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
  }

  upload.applyExifRotation = function (file) {
    if (file.type.indexOf('image/jpeg') !== 0) {
      return upload.emptyPromise(file);
    }

    var deferred = $q.defer();
    upload.readOrientation(file).then(function (result) {
      if (result.orientation < 2 || result.orientation > 8) {
        return deferred.resolve(file);
      }
      upload.dataUrl(file, true).then(function (url) {
        var canvas = document.createElement('canvas');
        var img = document.createElement('img');

        img.onload = function () {
          try {
            canvas.width = result.orientation > 4 ? img.height : img.width;
            canvas.height = result.orientation > 4 ? img.width : img.height;
            var ctx = canvas.getContext('2d');
            applyTransform(ctx, result.orientation, img.width, img.height);
            ctx.drawImage(img, 0, 0);
            var dataUrl = canvas.toDataURL(file.type || 'image/WebP', 0.934);
            dataUrl = upload.restoreExif(arrayBufferToBase64(result.fixedArrayBuffer), dataUrl);
            var blob = upload.dataUrltoBlob(dataUrl, file.name);
            deferred.resolve(blob);
          } catch (e) {
            return deferred.reject(e);
          }
        };
        img.onerror = function () {
          deferred.reject();
        };
        img.src = url;
      }, function (e) {
        deferred.reject(e);
      });
    }, function (e) {
      deferred.reject(e);
    });
    return deferred.promise;
  };

  upload.restoreExif = function (orig, resized) {
    var ExifRestorer = {};

    ExifRestorer.KEY_STR = 'ABCDEFGHIJKLMNOP' +
      'QRSTUVWXYZabcdef' +
      'ghijklmnopqrstuv' +
      'wxyz0123456789+/' +
      '=';

    ExifRestorer.encode64 = function (input) {
      var output = '',
        chr1, chr2, chr3 = '',
        enc1, enc2, enc3, enc4 = '',
        i = 0;

      do {
        chr1 = input[i++];
        chr2 = input[i++];
        chr3 = input[i++];

        enc1 = chr1 >> 2;
        enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
        enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
        enc4 = chr3 & 63;

        if (isNaN(chr2)) {
          enc3 = enc4 = 64;
        } else if (isNaN(chr3)) {
          enc4 = 64;
        }

        output = output +
          this.KEY_STR.charAt(enc1) +
          this.KEY_STR.charAt(enc2) +
          this.KEY_STR.charAt(enc3) +
          this.KEY_STR.charAt(enc4);
        chr1 = chr2 = chr3 = '';
        enc1 = enc2 = enc3 = enc4 = '';
      } while (i < input.length);

      return output;
    };

    ExifRestorer.restore = function (origFileBase64, resizedFileBase64) {
      if (origFileBase64.match('data:image/jpeg;base64,')) {
        origFileBase64 = origFileBase64.replace('data:image/jpeg;base64,', '');
      }

      var rawImage = this.decode64(origFileBase64);
      var segments = this.slice2Segments(rawImage);

      var image = this.exifManipulation(resizedFileBase64, segments);

      return 'data:image/jpeg;base64,' + this.encode64(image);
    };


    ExifRestorer.exifManipulation = function (resizedFileBase64, segments) {
      var exifArray = this.getExifArray(segments),
        newImageArray = this.insertExif(resizedFileBase64, exifArray);
      return new Uint8Array(newImageArray);
    };


    ExifRestorer.getExifArray = function (segments) {
      var seg;
      for (var x = 0; x < segments.length; x++) {
        seg = segments[x];
        if (seg[0] === 255 & seg[1] === 225) //(ff e1)
        {
          return seg;
        }
      }
      return [];
    };


    ExifRestorer.insertExif = function (resizedFileBase64, exifArray) {
      var imageData = resizedFileBase64.replace('data:image/jpeg;base64,', ''),
        buf = this.decode64(imageData),
        separatePoint = buf.indexOf(255, 3),
        mae = buf.slice(0, separatePoint),
        ato = buf.slice(separatePoint),
        array = mae;

      array = array.concat(exifArray);
      array = array.concat(ato);
      return array;
    };


    ExifRestorer.slice2Segments = function (rawImageArray) {
      var head = 0,
        segments = [];

      while (1) {
        if (rawImageArray[head] === 255 & rawImageArray[head + 1] === 218) {
          break;
        }
        if (rawImageArray[head] === 255 & rawImageArray[head + 1] === 216) {
          head += 2;
        }
        else {
          var length = rawImageArray[head + 2] * 256 + rawImageArray[head + 3],
            endPoint = head + length + 2,
            seg = rawImageArray.slice(head, endPoint);
          segments.push(seg);
          head = endPoint;
        }
        if (head > rawImageArray.length) {
          break;
        }
      }

      return segments;
    };


    ExifRestorer.decode64 = function (input) {
      var chr1, chr2, chr3 = '',
        enc1, enc2, enc3, enc4 = '',
        i = 0,
        buf = [];

      // remove all characters that are not A-Z, a-z, 0-9, +, /, or =
      var base64test = /[^A-Za-z0-9\+\/\=]/g;
      if (base64test.exec(input)) {
        console.log('There were invalid base64 characters in the input text.\n' +
          'Valid base64 characters are A-Z, a-z, 0-9, ' + ', ' / ',and "="\n' +
          'Expect errors in decoding.');
      }
      input = input.replace(/[^A-Za-z0-9\+\/\=]/g, '');

      do {
        enc1 = this.KEY_STR.indexOf(input.charAt(i++));
        enc2 = this.KEY_STR.indexOf(input.charAt(i++));
        enc3 = this.KEY_STR.indexOf(input.charAt(i++));
        enc4 = this.KEY_STR.indexOf(input.charAt(i++));

        chr1 = (enc1 << 2) | (enc2 >> 4);
        chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
        chr3 = ((enc3 & 3) << 6) | enc4;

        buf.push(chr1);

        if (enc3 !== 64) {
          buf.push(chr2);
        }
        if (enc4 !== 64) {
          buf.push(chr3);
        }

        chr1 = chr2 = chr3 = '';
        enc1 = enc2 = enc3 = enc4 = '';

      } while (i < input.length);

      return buf;
    };

    return ExifRestorer.restore(orig, resized);  //<= EXIF
  };

  return upload;
}]);

;'use strict';
angular.module("ngLocale", [], ["$provide", function($provide) {
var PLURAL_CATEGORY = {ZERO: "zero", ONE: "one", TWO: "two", FEW: "few", MANY: "many", OTHER: "other"};
function getDecimals(n) {
  n = n + '';
  var i = n.indexOf('.');
  return (i == -1) ? 0 : n.length - i - 1;
}

function getVF(n, opt_precision) {
  var v = opt_precision;

  if (undefined === v) {
    v = Math.min(getDecimals(n), 3);
  }

  var base = Math.pow(10, v);
  var f = ((n * base) | 0) % base;
  return {v: v, f: f};
}

$provide.value("$locale", {
  "DATETIME_FORMATS": {
    "AMPMS": [
      "vorm.",
      "nachm."
    ],
    "DAY": [
      "Sonntag",
      "Montag",
      "Dienstag",
      "Mittwoch",
      "Donnerstag",
      "Freitag",
      "Samstag"
    ],
    "ERANAMES": [
      "v. Chr.",
      "n. Chr."
    ],
    "ERAS": [
      "v. Chr.",
      "n. Chr."
    ],
    "FIRSTDAYOFWEEK": 0,
    "MONTH": [
      "Januar",
      "Februar",
      "M\u00e4rz",
      "April",
      "Mai",
      "Juni",
      "Juli",
      "August",
      "September",
      "Oktober",
      "November",
      "Dezember"
    ],
    "SHORTDAY": [
      "So.",
      "Mo.",
      "Di.",
      "Mi.",
      "Do.",
      "Fr.",
      "Sa."
    ],
    "SHORTMONTH": [
      "Jan.",
      "Feb.",
      "M\u00e4rz",
      "Apr.",
      "Mai",
      "Juni",
      "Juli",
      "Aug.",
      "Sep.",
      "Okt.",
      "Nov.",
      "Dez."
    ],
    "STANDALONEMONTH": [
      "Januar",
      "Februar",
      "M\u00e4rz",
      "April",
      "Mai",
      "Juni",
      "Juli",
      "August",
      "September",
      "Oktober",
      "November",
      "Dezember"
    ],
    "WEEKENDRANGE": [
      5,
      6
    ],
    "fullDate": "EEEE, d. MMMM y",
    "longDate": "d. MMMM y",
    "medium": "dd.MM.y HH:mm:ss",
    "mediumDate": "dd.MM.y",
    "mediumTime": "HH:mm:ss",
    "short": "dd.MM.yy HH:mm",
    "shortDate": "dd.MM.yy",
    "shortTime": "HH:mm"
  },
  "NUMBER_FORMATS": {
    "CURRENCY_SYM": "CHF",
    "DECIMAL_SEP": ".",
    "GROUP_SEP": "'",
    "PATTERNS": [
      {
        "gSize": 3,
        "lgSize": 3,
        "maxFrac": 3,
        "minFrac": 0,
        "minInt": 1,
        "negPre": "-",
        "negSuf": "",
        "posPre": "",
        "posSuf": ""
      },
      {
        "gSize": 3,
        "lgSize": 3,
        "maxFrac": 2,
        "minFrac": 2,
        "minInt": 1,
        "negPre": "\u00a4-",
        "negSuf": "",
        "posPre": "\u00a4\u00a0",
        "posSuf": ""
      }
    ]
  },
  "id": "de-ch",
  "localeID": "de_CH",
  "pluralCat": function(n, opt_precision) {  var i = n | 0;  var vf = getVF(n, opt_precision);  if (i == 1 && vf.v == 0) {    return PLURAL_CATEGORY.ONE;  }  return PLURAL_CATEGORY.OTHER;}
});
}]);
;(function() {
  var app;

  app = angular.module('js.darg.api', ['ngResource']);

  app.factory('Shareholder', [
    '$resource', function($resource) {
      return $resource('/services/rest/shareholders/:id', {
        id: '@pk'
      }, {
        update: {
          method: 'PUT'
        }
      });
    }
  ]);

  app.factory('Security', [
    '$resource', function($resource) {
      return $resource('/services/rest/security/:id', {
        id: '@pk'
      }, {
        update: {
          method: 'PUT'
        }
      });
    }
  ]);

  app.factory('CompanyAdd', [
    '$resource', function($resource) {
      return $resource('/services/rest/company/add/');
    }
  ]);

  app.factory('Company', [
    '$resource', function($resource) {
      return $resource('/services/rest/company/:id', {
        id: '@pk'
      }, {
        update: {
          method: 'PUT'
        }
      });
    }
  ]);

  app.factory('Country', [
    '$resource', function($resource) {
      return $resource('/services/rest/country/:id', {
        id: '@pk'
      }, {
        update: {
          method: 'PUT'
        }
      });
    }
  ]);

  app.factory('User', [
    '$resource', function($resource) {
      return $resource('/services/rest/user/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('Position', [
    '$resource', function($resource) {
      return $resource('/services/rest/position/:id', {
        id: '@id'
      }, {
        invalidate: {
          method: 'GET',
          url: '/services/rest/position/:id/invalidate'
        }
      });
    }
  ]);

  app.factory('Split', [
    '$resource', function($resource) {
      return $resource('/services/rest/split/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('Operator', [
    '$resource', function($resource) {
      return $resource('/services/rest/operators/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('OptionPlan', [
    '$resource', function($resource) {
      return $resource('/services/rest/optionplan/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('OptionTransaction', [
    '$resource', function($resource) {
      return $resource('/services/rest/optiontransaction/:id', {
        id: '@id'
      });
    }
  ]);

  app.factory('Invitee', [
    '$resource', function($resource) {
      return $resource('/services/rest/invitee/:id', {
        id: '@id'
      });
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.base', ['js.darg.api']);

  app.controller('BaseController', [
    '$scope', '$http', function($scope, $http) {
      return this.scope.test = True;
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.company', ['js.darg.api', 'xeditable', 'ngFileUpload', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('CompanyController', [
    '$scope', '$http', '$window', 'Company', 'Country', 'Operator', 'Upload', 'Security', '$timeout', function($scope, $http, $window, Company, Country, Operator, Upload, Security, $timeout) {
      $scope.operators = [];
      $scope.company = null;
      $scope.errors = null;
      $scope.show_add_operator_form = false;
      $scope.file = null;
      $scope.logo_success = false;
      $scope.logo_errors = false;
      $scope.loading = false;
      $scope.newOperator = new Operator();
      $http.get('/services/rest/company/' + company_id).then(function(result) {
        $scope.company = new Company(result.data);
        $scope.company.founded_at = new Date($scope.company.founded_at);
        if ($scope.company.country) {
          return $http.get($scope.company.country).then(function(result1) {
            return $scope.company.country = result1.data;
          });
        }
      });
      $http.get('/services/rest/country').then(function(result) {
        return $scope.countries = result.data.results;
      });
      $http.get('/services/rest/operators').then(function(result) {
        return $scope.operators = result.data.results;
      });
      $scope.toggle_add_operator_form = function() {
        if ($scope.show_add_operator_form) {
          return $scope.show_add_operator_form = false;
        } else {
          return $scope.show_add_operator_form = true;
        }
      };
      $scope.delete_operator = function(pk) {
        return $http["delete"]('/services/rest/operators/' + pk).then(function() {
          return $http.get('/services/rest/operators').then(function(result) {
            return $scope.operators = result.data.results;
          });
        });
      };
      $scope.add_operator = function() {
        $scope.newOperator.company = $scope.company.url;
        return $scope.newOperator.$save().then(function(result) {
          return $http.get('/services/rest/operators').then(function(result) {
            return $scope.operators = result.data.results;
          });
        }).then(function() {
          return $scope.newOperator = new Operator();
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          $scope.errors = rejection.data;
          return Raven.captureMessage('add operator form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.edit_security = function(security) {
        var sec;
        sec = new Security(security);
        return sec.$update().then(function(result) {
          var i;
          i = $scope.company.security_set.indexOf(security);
          return $scope.company.security_set[i] = result;
        }, function(rejection) {
          return rejection.data.number_segments[0];
        });
      };
      $scope.edit_company = function() {
        if ($scope.company.country) {
          $scope.company.country = $scope.company.country.url;
        }
        if ($scope.company.founded_at) {
          $scope.company.founded_at = $scope.company.founded_at.toISOString().substring(0, 10);
        }
        return $scope.company.$update().then(function(result) {
          result.founded_at = new Date(result.founded_at);
          $scope.company = new Company(result);
          return $http.get($scope.company.country).then(function(result1) {
            return $scope.company.country = result1.data;
          });
        }).then(function() {
          return void 0;
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          $scope.company.founded_at = new Date($scope.company.founded_at);
          $scope.errors = rejection.data;
          return Raven.captureMessage('add corp form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.$watch('files', function() {
        $scope.upload($scope.files);
      });
      $scope.$watch('file', function() {
        if ($scope.file !== null) {
          $scope.files = [$scope.file];
        }
      });
      $scope.upload = function(files) {
        var file, i, payload;
        if (files && files.length) {
          $scope.loading = true;
          i = 0;
          while (i < files.length) {
            file = files[i];
            if (!file.$error) {
              payload = $scope.company;
              payload.founded_at = $scope.company.founded_at.toISOString().substring(0, 10);
              payload.logo = file;
              Upload.upload({
                url: '/services/rest/company/' + company_id + '/upload',
                data: payload,
                objectKey: '.k'
              }).then((function(response) {
                $timeout(function() {
                  var company;
                  company = new Company(response.data);
                  company.founded_at = new Date(company.founded_at);
                  $scope.company = company;
                  $scope.logo_success = true;
                  $scope.logo_errors = false;
                });
                return $timeout(function() {
                  $scope.logo_success = false;
                  return $scope.loading = false;
                }, 3000);
              }), (function(response) {
                return $timeout(function() {
                  $scope.logo_errors = response.data;
                  return $scope.loading = false;
                });
              }), function(evt) {
                Raven.captureException(evt, {
                  level: 'warning'
                });
              });
              return;
            }
          }
        }
      };
      $scope.datepicker = {
        opened: false
      };
      $scope.datepicker.format = 'd.MM.yy';
      $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      $scope.open_datepicker = function() {
        return $scope.datepicker.opened = true;
      };
      return $scope.confirm_company_reset = function() {
        var label;
        $scope.errors = [];
        if ($scope.confirmCompanyText === gettext('DELETE')) {
          return $scope.company.$delete().then(function() {
            $('#companyResetModal').modal('hide');
            if (!_.isUndefined(window.ga)) {
              ga('send', 'event', 'click', 'delete', 'company');
            }
            return $window.location.href = '/start/';
          });
        } else {
          label = gettext('Input');
          $scope.errors = {};
          return $scope.errors[label] = [gettext('Please enter DELETE')];
        }
      };
    }
  ]);

  app.run(function(editableOptions) {
    editableOptions.theme = 'bs3';
  });

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.index', ['js.darg.api']);

  app.controller('IndexController', [
    '$scope', '$http', 'Invitee', function($scope, $http, Invitee) {
      $scope.show_add_invitee = true;
      $scope.newInvitee = new Invitee();
      $scope.errors = [];
      return $scope.add_invitee = function() {
        return $scope.newInvitee.$save().then(function(result) {
          $scope.show_add_invitee = false;
          if (!_.isUndefined(window.ga)) {
            return ga('send', 'event', 'click', 'save_invitee_email');
          }
        }).then(function() {
          return $scope.newInvitee = new Invitee();
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          return $scope.errors = rejection.data;
        });
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.options', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('OptionsController', [
    '$scope', '$http', '$window', '$filter', 'OptionPlan', 'OptionTransaction', '$timeout', function($scope, $http, $window, $filter, OptionPlan, OptionTransaction, $timeout) {
      $scope.option_plans = [];
      $scope.optiontransactions = [];
      $scope.securities = [];
      $scope.loading = true;
      $scope.transaction_added_success = false;
      $scope.plan_added_success = false;
      $scope.show_add_option_transaction = false;
      $scope.show_add_option_plan = false;
      $scope.show_optional_fields = false;
      $scope.newOptionPlan = new OptionPlan();
      $scope.newOptionPlan.board_approved_at = new Date();
      $scope.newOptionTransaction = new OptionTransaction();
      $scope.newOptionTransaction.bought_at = new Date();
      $scope.depot_types = [
        {
          name: gettext('Sperrdepot'),
          value: '2'
        }, {
          name: gettext('Zertifikatsdepot'),
          value: '0'
        }, {
          name: gettext('Gesellschaftsdepot'),
          value: '1'
        }
      ];
      $scope.next = false;
      $scope.previous = false;
      $scope.total = 0;
      $scope.current = 0;
      $scope.current_range = '';
      $scope.search_params = {
        'query': null,
        'ordering': null,
        'ordering_reverse': null
      };
      $scope.ordering_options = false;
      $scope.numberSegmentsAvailable = '';
      $scope.hasSecurityWithTrackNumbers = function() {
        var s;
        s = $scope.securities.find(function(el) {
          return el.track_numbers === true;
        });
        if (s !== void 0) {
          return true;
        }
      };
      $scope.$watchCollection('current', function(current) {
        var end, start;
        start = ($scope.current - 1) * 20;
        end = Math.min($scope.current * 20, $scope.total);
        return $scope.current_range = start.toString() + '-' + end.toString();
      });
      $scope.reset_search_params = function() {
        $scope.current = null;
        $scope.previous = null;
        $scope.next = null;
        $scope.optiontransactions = [];
        return $scope.option_plans = [];
      };
      $scope.load_all = function() {
        $scope.reset_search_params();
        $scope.search_params.query = null;
        $http.get('/services/rest/optiontransaction').then(function(result) {
          angular.forEach(result.data.results, function(item) {
            return $scope.optiontransactions.push(item);
          });
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            return $scope.current = result.data.current;
          }
        })["finally"](function() {
          return $scope.loading = false;
        });
        return $http.get('/services/rest/optionplan').then(function(result) {
          return angular.forEach(result.data.results, function(item) {
            return $scope.option_plans.push(item);
          });
        });
      };
      $scope.load_all();
      $http.get('/services/rest/security').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.securities.push(item);
        });
      });
      $scope.next_page = function() {
        if ($scope.next) {
          return $http.get($scope.next).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.optiontransactions.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.previous_page = function() {
        if ($scope.previous) {
          return $http.get($scope.previous).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.optiontransactions.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.search_shareholders = function(term) {
        var paramss;
        paramss = {
          search: term
        };
        return $http.get('/services/rest/shareholders', {
          params: paramss
        }).then(function(response) {
          return response.data.results.map(function(item) {
            return item;
          });
        });
      };
      $scope.search = function() {
        var params, paramss;
        params = {};
        if ($scope.search_params.query) {
          params.search = $scope.search_params.query;
        }
        if ($scope.search_params.ordering) {
          params.ordering = $scope.search_params.ordering;
        }
        paramss = $.param(params);
        console.log(params);
        return $http.get('/services/rest/optiontransaction?' + paramss).then(function(result) {
          $scope.reset_search_params();
          angular.forEach(result.data.results, function(item) {
            return $scope.optiontransactions.push(item);
          });
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            $scope.current = result.data.current;
          }
          return $scope.search_params.query = params.search;
        });
      };
      $scope.add_option_plan = function() {
        var date;
        if ($scope.newOptionPlan.board_approved_at) {
          date = $scope.newOptionPlan.board_approved_at;
          date.setHours(date.getHours() - date.getTimezoneOffset() / 60);
          $scope.newOptionPlan.board_approved_at = date.toISOString().substring(0, 10);
        }
        return $scope.newOptionPlan.$save().then(function(result) {
          return $scope.load_all();
        }).then(function() {
          $scope.newOptionPlan = new OptionPlan();
          $scope.show_add_option_plan = false;
          $scope.plan_added_success = true;
          return $timeout(function() {
            return $scope.plan_added_success = false;
          }, 5000);
        }).then(function() {
          $scope.errors = null;
          return $window.ga('send', 'event', 'form-send', 'add-optionplan');
        }, function(rejection) {
          $scope.errors = rejection.data;
          Raven.captureMessage('add option plan form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
          if (date) {
            return $scope.newOptionPlan.board_approved_at = date;
          }
        });
      };
      $scope.add_option_transaction = function() {
        var date, p;
        if ($scope.newOptionTransaction.option_plan) {
          p = $scope.newOptionTransaction.option_plan;
        }
        if ($scope.newOptionTransaction.bought_at) {
          date = $scope.newOptionTransaction.bought_at;
          date.setHours(date.getHours() - date.getTimezoneOffset() / 60);
          $scope.newOptionTransaction.bought_at = date.toISOString().substring(0, 10);
        }
        if ($scope.newOptionTransaction.depot_type) {
          $scope.newOptionTransaction.depot_type = $scope.newOptionTransaction.depot_type.value;
        }
        return $scope.newOptionTransaction.$save().then(function(result) {
          return $scope.load_all();
        }).then(function() {
          $scope.newOptionTransaction = new OptionTransaction();
          $scope.show_add_option_transaction = false;
          $scope.transaction_added_success = true;
          return $timeout(function() {
            return $scope.transaction_added_success = false;
          }, 5000);
        }).then(function() {
          $scope.errors = null;
          return $window.ga('send', 'event', 'form-send', 'add-option-transaction');
        }, function(rejection) {
          $scope.errors = rejection.data;
          Raven.captureMessage('add option transaction form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
          $scope.newOptionTransaction.bought_at = date;
          return $scope.newOptionTransaction.option_plan = p;
        });
      };
      $scope.delete_option_transaction = function(option_transaction) {
        return $http["delete"]('/services/rest/optiontransaction/' + option_transaction.pk).then(function(result) {
          return $scope.load_all();
        });
      };
      $scope.confirm_option_transaction = function(option_transaction) {
        return $http.post('/services/rest/optiontransaction/' + option_transaction.pk + '/confirm').then(function(result) {
          return $scope.load_all();
        });
      };
      $scope.show_add_option_plan_form = function() {
        $scope.show_add_option_plan = true;
        $scope.show_add_option_transaction = false;
        return $scope.newOptionPlan = new OptionPlan();
      };
      $scope.show_add_option_transaction_form = function() {
        $scope.show_add_option_transaction = true;
        $scope.show_add_option_plan = false;
        return $scope.newOptionTransaction = new OptionTransaction();
      };
      $scope.hide_form = function() {
        $scope.show_add_option_plan = false;
        $scope.show_add_option_transaction = false;
        $scope.newOptionPlan = new OptionPlan();
        return $scope.newOptionTransaction = new OptionTransaction();
      };
      $scope.show_available_number_segments_for_new_option_plan = function() {
        var url;
        if ($scope.newOptionPlan.security) {
          if ($scope.newOptionPlan.security.track_numbers) {
            url = '/services/rest/shareholders/company_number_segments';
            if ($scope.newOptionPlan.board_approved_at) {
              url = url + '?date=' + $scope.newOptionPlan.board_approved_at.toISOString();
            }
            return $http.get(url).then(function(result) {
              if ($scope.newOptionPlan.security.pk in result.data && result.data[$scope.newOptionPlan.security.pk].length > 0) {
                return $scope.numberSegmentsAvailable = gettext('Available security segments for option plan on selected date or now: ') + result.data[$scope.newOptionPlan.security.pk];
              } else {
                return $scope.numberSegmentsAvailable = gettext('Available security segments for option plan on selected date or now: None');
              }
            });
          } else {
            return $scope.numberSegmentsAvailable = '';
          }
        }
      };
      $scope.show_available_number_segments_for_new_option_transaction = function() {
        var op_pk, sh_pk, url;
        if ($scope.newOptionTransaction.seller && $scope.newOptionTransaction.option_plan && $scope.newOptionTransaction.option_plan.security.track_numbers) {
          op_pk = $scope.newOptionTransaction.option_plan.pk.toString();
          sh_pk = $scope.newOptionTransaction.seller.pk.toString();
          url = '/services/rest/optionplan/' + op_pk + '/number_segments/' + sh_pk;
          if ($scope.newOptionTransaction.bought_at) {
            url = url + '?date=' + $scope.newOptionTransaction.bought_at.toISOString();
          }
          return $http.get(url).then(function(result) {
            if (result.data && result.data.length > 0) {
              return $scope.numberSegmentsAvailable = gettext('Available security segments for option plan on selected date or now: ') + result.data;
            } else {
              return $scope.numberSegmentsAvailable = gettext('No security segments available for option plan on selected date or now.');
            }
          });
        }
      };
      $scope.toggle_optional_fields = function() {
        if ($scope.show_optional_fields) {
          return $scope.show_optional_fields = false;
        } else {
          return $scope.show_optional_fields = true;
        }
      };
      $scope.datepicker = {
        opened: false
      };
      $scope.datepicker.format = 'd. MMM yyyy';
      $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      $scope.toggle_datepicker = function() {
        return $scope.datepicker.opened = !$scope.datepicker.opened;
      };
      return $scope.goto_option = function(option_id) {
        return window.location = "/options/" + option_id + "/";
      };
    }
  ]);

  app.directive('stringToNumber', function() {
    return {
      require: 'ngModel',
      link: function(scope, element, attrs, ngModel) {
        ngModel.$parsers.push(function(value) {
          return '' + value;
        });
        ngModel.$formatters.push(function(value) {
          return parseFloat(value);
        });
      }
    };
  });

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.optionplan', ['js.darg.api', 'xeditable', 'ngFileUpload', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('OptionPlanController', [
    '$scope', '$http', 'OptionPlan', 'Upload', '$timeout', function($scope, $http, OptionPlan, Upload, $timeout) {
      $scope.file = null;
      $scope.pdf_upload_success = false;
      $scope.pdf_upload_errors = false;
      $scope.loading = false;
      $http.get('/services/rest/optionplan/' + optionplan_id).then(function(result) {
        $scope.optionplan = new OptionPlan(result.data);
        return $scope.optionplan.board_approved_at = $scope.optionplan.board_approved_at;
      });
      $http.get('/services/rest/security').then(function(result) {
        return $scope.securities = result.data.results;
      });
      $scope.$watch('files', function() {
        $scope.upload($scope.files);
      });
      $scope.$watch('file', function() {
        if ($scope.file !== null) {
          $scope.files = [$scope.file];
        }
      });
      return $scope.upload = function(files) {
        var file, i, payload;
        if (files && files.length) {
          $scope.loading = true;
          i = 0;
          while (i < files.length) {
            file = files[i];
            if (!file.$error) {
              payload = $scope.optionplan;
              payload.pdf_file = file;
              Upload.upload({
                url: '/services/rest/optionplan/' + optionplan_id + '/upload',
                data: payload,
                objectKey: '.k'
              }).then((function(response) {
                $timeout(function() {
                  $scope.optionplan = response.data;
                  $scope.pdf_upload_success = true;
                  $scope.pdf_upload_errors = false;
                });
                return $timeout(function() {
                  $scope.pdf_upload_success = false;
                  return $scope.loading = false;
                }, 3000);
              }), (function(response) {
                return $timeout(function() {
                  $scope.pdf_upload_errors = response.data;
                  return $scope.loading = false;
                });
              }), function(evt) {
                Raven.captureException(evt, {
                  level: 'warning'
                });
              });
              return;
            }
          }
        }
      };
    }
  ]);

  app.run(function(editableOptions) {
    editableOptions.theme = 'bs3';
  });

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.optiontransaction', ['js.darg.api', 'xeditable', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('OptionTransactionController', [
    '$scope', '$http', 'OptionTransaction', function($scope, $http, OptionTransaction) {
      $scope.optiontransaction = true;
      return $http.get('/services/rest/optiontransaction/' + optiontransaction_id).then(function(result) {
        return $scope.optiontransaction = new OptionTransaction(result.data);
      });
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.position', ['js.darg.api', 'xeditable', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('PositionController', [
    '$scope', '$http', 'Position', function($scope, $http, Position) {
      $scope.position = null;
      $scope.errors = null;
      $scope.load_position = function() {
        return $http.get('/services/rest/position/' + position_id).then(function(result) {
          return $scope.position = new Position(result.data);
        });
      };
      $scope.load_position();
      return $scope.invalidate_certificate = function() {
        if ($scope.position) {
          return $scope.position.$invalidate({
            id: position_id
          }).then(function(result) {
            return $scope.position = result;
          }, function(rejection) {
            return Raven.captureMessage('invalidate certificate error: ' + rejection.statusText, {
              level: 'warning',
              extra: {
                rejection: rejection
              }
            });
          });
        }
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.positions', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('PositionsController', [
    '$scope', '$http', '$window', 'Position', 'Split', '$timeout', function($scope, $http, $window, Position, Split, $timeout) {
      $scope.positions = [];
      $scope.securities = [];
      $scope.position_added_success = false;
      $scope.split_added_success = false;
      $scope.show_add_position = false;
      $scope.show_add_capital = false;
      $scope.show_split_data = false;
      $scope.show_split = false;
      $scope.show_optional_fields = false;
      $scope.newPosition = new Position();
      $scope.newSplit = new Split();
      $scope.depot_types = [
        {
          name: gettext('Sperrdepot'),
          value: '2'
        }, {
          name: gettext('Zertifikatsdepot'),
          value: '0'
        }, {
          name: gettext('Gesellschaftsdepot'),
          value: '1'
        }
      ];
      $scope.next = false;
      $scope.previous = false;
      $scope.total = 0;
      $scope.current = 0;
      $scope.current_range = '';
      $scope.search_params = {
        'query': null,
        'ordering': null,
        'ordering_reverse': null
      };
      $scope.ordering_options = false;
      $scope.numberSegmentsAvailable = '';
      $scope.hasSecurityWithTrackNumbers = function() {
        var s;
        s = $scope.securities.find(function(el) {
          return el.track_numbers === true;
        });
        if (s !== void 0) {
          return true;
        }
      };
      $scope.positionsLoading = true;
      $scope.addPositionLoading = false;
      $scope.$watchCollection('current', function(current) {
        var end, start;
        start = ($scope.current - 1) * 20;
        end = Math.min($scope.current * 20, $scope.total);
        return $scope.current_range = start.toString() + '-' + end.toString();
      });
      $scope.reset_search_params = function() {
        $scope.current = null;
        $scope.previous = null;
        $scope.next = null;
        return $scope.positions = [];
      };
      $scope.load_all_positions = function() {
        $scope.reset_search_params();
        $scope.search_params.query = null;
        return $http.get('/services/rest/position').then(function(result) {
          angular.forEach(result.data.results, function(item) {
            return $scope.positions.push(item);
          });
          $scope.positionsLoading = false;
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            return $scope.current = result.data.current;
          }
        });
      };
      $scope.load_all_positions();
      $http.get('/services/rest/security').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.securities.push(item);
        });
      });
      $scope.next_page = function() {
        if ($scope.next) {
          return $http.get($scope.next).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.positions.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.previous_page = function() {
        if ($scope.previous) {
          return $http.get($scope.previous).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.positions.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.search_shareholders = function(term) {
        var paramss;
        paramss = {
          search: term
        };
        return $http.get('/services/rest/shareholders', {
          params: paramss
        }).then(function(response) {
          return response.data.results.map(function(item) {
            return item;
          });
        });
      };
      $scope.search_banks = function(term) {
        var paramss;
        paramss = {
          search: term
        };
        return $http.get('/services/rest/bank', {
          params: paramss
        }).then(function(response) {
          return response.data.results.map(function(item) {
            return item;
          });
        });
      };
      $scope.search = function() {
        var params, paramss;
        params = {};
        if ($scope.search_params.query) {
          params.search = $scope.search_params.query;
        }
        if ($scope.search_params.ordering) {
          params.ordering = $scope.search_params.ordering;
        }
        paramss = $.param(params);
        return $http.get('/services/rest/position', {
          params: params
        }).then(function(result) {
          $scope.reset_search_params();
          angular.forEach(result.data.results, function(item) {
            return $scope.positions.push(item);
          });
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            $scope.current = result.data.current;
          }
          return $scope.search_params.query = params.search;
        });
      };
      $scope.add_position = function() {
        var bought_at;
        $scope.addPositionLoading = true;
        if ($scope.newPosition.bought_at) {
          bought_at = $scope.newPosition.bought_at;
          bought_at.setHours(bought_at.getHours() - bought_at.getTimezoneOffset() / 60);
          $scope.newPosition.bought_at = bought_at;
        }
        if ($scope.newPosition.depot_type) {
          $scope.newPosition.depot_type = $scope.newPosition.depot_type.value;
        }
        return $scope.newPosition.$save().then(function(result) {
          return $scope.positions.push(result);
        }).then(function() {
          $scope.show_add_position = false;
          $scope.show_add_capital = false;
          $scope.newPosition = new Position();
          $scope.position_added_success = true;
          return $timeout(function() {
            return $scope.position_added_success = false;
          }, 5000);
        }).then(function() {
          $scope.errors = null;
          $window.ga('send', 'event', 'form-send', 'add-transaction');
          return $scope.addPositionLoading = false;
        }, function(rejection) {
          $scope.errors = rejection.data;
          Raven.captureMessage('add position form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
          return $scope.addPositionLoading = false;
        });
      };
      $scope.delete_position = function(position) {
        $scope.positionsLoading = true;
        return $http["delete"]('/services/rest/position/' + position.pk).then(function(result) {
          $scope.positions = [];
          $http.get('/services/rest/position').then(function(result1) {
            return angular.forEach(result1.data.results, function(item) {
              return $scope.positions.push(item);
            });
          });
          return $scope.positionsLoading = false;
        });
      };
      $scope.confirm_position = function(position) {
        return $http.post('/services/rest/position/' + position.pk + '/confirm').then(function(result) {
          $scope.positions = [];
          return $http.get('/services/rest/position').then(function(result1) {
            angular.forEach(result1.data.results, function(item) {
              return $scope.positions.push(item);
            });
            return $scope.positionsLoading = false;
          });
        });
      };
      $scope.add_split = function() {
        var execute_at;
        execute_at = $scope.newSplit.execute_at;
        execute_at.setHours(execute_at.getHours() - execute_at.getTimezoneOffset() / 60);
        $scope.newSplit.execute_at = execute_at;
        return $scope.newSplit.$save().then(function(result) {
          return $scope.positions = result.data;
        }).then(function() {
          $scope.newSplit = new Split();
          $scope.split_added_success = true;
          return $timeout(function() {
            return $scope.split_added_success = false;
          }, 5000);
        }).then(function() {
          $scope.errors = null;
          $scope.show_split = false;
          return $window.ga('send', 'event', 'form-send', 'add-split');
        }, function(rejection) {
          $scope.errors = rejection.data;
          return Raven.captureMessage('add split form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.get_new_certificate_id = function() {
        return $http({
          method: 'GET',
          url: '/services/rest/position/get_new_certificate_id'
        }).then((function(response) {
          return $scope.newPosition.certificate_id = response.data.certificate_id;
        }), function(response) {
          return $scope.errors = response.errors;
        });
      };
      $scope.show_add_position_form = function() {
        $scope.show_add_position = true;
        $scope.show_add_capital = false;
        $scope.newPosition = new Position();
        return $scope.show_split = false;
      };
      $scope.toggle_show_split_data = function() {
        if ($scope.show_split_data) {
          return $scope.show_split_data = false;
        } else {
          return $scope.show_split_data = true;
        }
      };
      $scope.toggle_optional_fields = function() {
        if ($scope.show_optional_fields) {
          return $scope.show_optional_fields = false;
        } else {
          return $scope.show_optional_fields = true;
        }
      };
      $scope.show_add_capital_form = function() {
        $scope.show_add_position = false;
        $scope.show_add_capital = true;
        $scope.newPosition = new Position();
        return $scope.show_split = false;
      };
      $scope.hide_form = function() {
        $scope.show_add_position = false;
        $scope.show_add_capital = false;
        $scope.newPosition = new Position();
        return $scope.show_split = false;
      };
      $scope.show_split_form = function() {
        $scope.show_add_position = false;
        $scope.show_add_capital = false;
        $scope.newSplit = new Split();
        return $scope.show_split = true;
      };
      $scope.show_available_number_segments = function() {
        var url;
        if ($scope.newPosition.security) {
          if ($scope.newPosition.security.track_numbers && $scope.newPosition.seller) {
            url = '/services/rest/shareholders/' + $scope.newPosition.seller.pk.toString() + '/number_segments';
            if ($scope.newPosition.bought_at) {
              url = url + '?date=' + $scope.newPosition.bought_at.toISOString();
            }
            return $http.get(url).then(function(result) {
              if ($scope.newPosition.security.pk in result.data && result.data[$scope.newPosition.security.pk].length > 0) {
                return $scope.numberSegmentsAvailable = gettext('Available security segments from this shareholder on selected date or now: ') + result.data[$scope.newPosition.security.pk];
              } else {
                return $scope.numberSegmentsAvailable = gettext('Available security segments from this shareholder on selected date or now: None');
              }
            });
          }
        }
      };
      $scope.datepicker = {
        opened: false
      };
      $scope.datepicker.format = 'd. MMM yyyy';
      $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      $scope.toggle_datepicker = function() {
        return $scope.datepicker.opened = !$scope.datepicker.opened;
      };
      return $scope.goto_position = function(position_id) {
        return window.location = "/positions/" + position_id + "/";
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.reports', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('ReportsController', [
    '$scope', '$http', 'Shareholder', function($scope, $http, Shareholder) {
      $scope.transactions_download_params = {};
      $scope.securities = [];
      $scope.show_transaction_form = false;
      $scope.enable_transaction_download = false;
      $scope.transaction_download_url = '';
      $scope.show_captable_form = false;
      $scope.captable_orderings = [
        {
          title: gettext('Last Name'),
          value: 'user__last_name'
        }, {
          title: gettext('Last Name (descending)'),
          value: 'user__last_name_desc'
        }, {
          title: gettext('Share Count'),
          value: 'share_count'
        }, {
          title: gettext('Share Count (descending)'),
          value: 'share_count_desc'
        }, {
          title: gettext('Shareholder Number'),
          value: 'number'
        }, {
          title: gettext('Shareholder Number (descending)'),
          value: 'number_desc'
        }, {
          title: gettext('Share Percent Ownership'),
          value: 'share_percent'
        }, {
          title: gettext('Share Percent Ownership (descending)'),
          value: 'share_percent_desc'
        }
      ];
      $scope.captable_report = {
        ordering: $scope.captable_orderings[6]
      };
      $scope.captable_csv_url = '';
      $scope.captable_pdf_url = '';
      $http.get('/services/rest/security').then(function(result) {
        return angular.forEach(result.data.results, function(item) {
          return $scope.securities.push(item);
        });
      });
      $scope.$watchCollection('transactions_download_params', function(transactions_download_params) {
        if (transactions_download_params.to && transactions_download_params.from && transactions_download_params.security) {
          $scope.enable_transaction_download = true;
          return $scope.transaction_download_url = '/company/' + company_id + '/download/transactions?from=' + $scope.transactions_download_params.from.toISOString() + '&to=' + $scope.transactions_download_params.to.toISOString() + '&security=' + $scope.transactions_download_params.security.pk;
        }
      });
      $scope.$watchCollection('captable_report', function(captable_report) {
        var ext;
        ext = '';
        if (captable_report.ordering) {
          ext = '?ordering=' + captable_report.ordering.value;
        }
        $scope.captable_csv_url = '/company/' + company_id + '/download/pdf' + ext;
        return $scope.captable_pdf_url = '/company/' + company_id + '/download/csv' + ext;
      });
      $scope.toggle_transaction_form = function() {
        if ($scope.show_transaction_form) {
          return $scope.show_transaction_form = false;
        } else {
          return $scope.show_transaction_form = true;
        }
      };
      $scope.toggle_captable_form = function() {
        if ($scope.show_captable_form) {
          return $scope.show_captable_form = false;
        } else {
          return $scope.show_captable_form = true;
        }
      };
      $scope.datepicker1 = {
        opened: false
      };
      $scope.datepicker1.format = 'd. MMM yyyy';
      $scope.datepicker1.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      $scope.toggle_datepicker1 = function() {
        return $scope.datepicker1.opened = !$scope.datepicker1.opened;
      };
      $scope.datepicker2 = {
        opened: false
      };
      $scope.datepicker2.format = 'd. MMM yyyy';
      $scope.datepicker2.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      return $scope.toggle_datepicker2 = function() {
        return $scope.datepicker2.opened = !$scope.datepicker2.opened;
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.select_company', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('SelectCompanyController', ['$scope', '$http', function($scope, $http) {}]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.shareholder', ['js.darg.api', 'xeditable', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('ShareholderController', [
    '$scope', '$http', 'Shareholder', function($scope, $http, Shareholder) {
      $scope.shareholder = true;
      $scope.countries = [];
      $scope.languages = [];
      $scope.errors = null;
      $scope.legal_types = [
        {
          name: gettext('Human Being'),
          value: 'H'
        }, {
          name: gettext('Corporate'),
          value: 'C'
        }
      ];
      $scope.mailing_types = [
        {
          name: gettext('Not deliverable'),
          value: '0'
        }, {
          name: gettext('Postal Mail'),
          value: '1'
        }, {
          name: gettext('via Email'),
          value: '2'
        }
      ];
      $http.get('/services/rest/language').then(function(result_lang) {
        return $scope.languages = result_lang.data;
      });
      $http.get('/services/rest/shareholders/' + shareholder_id).then(function(result) {
        var language, legal_type, mailing_type;
        if (result.data.user.userprofile.birthday !== null) {
          result.data.user.userprofile.birthday = new Date(result.data.user.userprofile.birthday);
        }
        $scope.shareholder = new Shareholder(result.data);
        if ($scope.shareholder.user.userprofile.country) {
          $http.get($scope.shareholder.user.userprofile.country).then(function(result1) {
            return $scope.shareholder.user.userprofile.country = result1.data;
          });
        }
        if ($scope.shareholder.user.userprofile.nationality) {
          $http.get($scope.shareholder.user.userprofile.nationality).then(function(result1) {
            return $scope.shareholder.user.userprofile.nationality = result1.data;
          });
        }
        legal_type = $scope.legal_types.filter(function(obj) {
          return obj.value === $scope.shareholder.user.userprofile.legal_type;
        });
        $scope.shareholder.user.userprofile.legal_type = legal_type[0];
        mailing_type = $scope.mailing_types.filter(function(obj) {
          return obj.value === $scope.shareholder.mailing_type;
        });
        $scope.shareholder.mailing_type = mailing_type[0];
        if ($scope.shareholder.user.userprofile.language) {
          language = $scope.languages.filter(function(obj) {
            return obj.iso === $scope.shareholder.user.userprofile.language;
          });
          return $scope.shareholder.user.userprofile.language = language[0];
        }
      });
      $http.get('/services/rest/country').then(function(result) {
        return $scope.countries = result.data.results;
      });
      $scope.edit_shareholder = function() {
        var date;
        if ($scope.shareholder.user.userprofile.birthday) {
          date = $scope.shareholder.user.userprofile.birthday;
          date.setHours(date.getHours() - date.getTimezoneOffset() / 60);
          $scope.shareholder.user.userprofile.birthday = date;
        }
        if ($scope.shareholder.user.userprofile.country) {
          $scope.shareholder.user.userprofile.country = $scope.shareholder.user.userprofile.country.url;
        }
        if ($scope.shareholder.user.userprofile.nationality) {
          $scope.shareholder.user.userprofile.nationality = $scope.shareholder.user.userprofile.nationality.url;
        }
        if ($scope.shareholder.user.userprofile.language) {
          $scope.shareholder.user.userprofile.language = $scope.shareholder.user.userprofile.language.iso;
        }
        if ($scope.shareholder.user.userprofile.legal_type) {
          $scope.shareholder.user.userprofile.legal_type = $scope.shareholder.user.userprofile.legal_type.value;
        }
        if ($scope.shareholder.mailing_type) {
          $scope.shareholder.mailing_type = $scope.shareholder.mailing_type.value;
        }
        return $scope.shareholder.$update().then(function(result) {
          var language, legal_type;
          if (result.user.userprofile.birthday !== null) {
            result.user.userprofile.birthday = new Date(result.user.userprofile.birthday);
          }
          $scope.shareholder = new Shareholder(result);
          if ($scope.shareholder.user.userprofile.country) {
            $http.get($scope.shareholder.user.userprofile.country).then(function(result1) {
              return $scope.shareholder.user.userprofile.country = result1.data;
            });
          }
          if ($scope.shareholder.user.userprofile.nationality) {
            $http.get($scope.shareholder.user.userprofile.nationality).then(function(result1) {
              return $scope.shareholder.user.userprofile.nationality = result1.data;
            });
          }
          if ($scope.shareholder.user.userprofile.legal_type) {
            legal_type = $scope.legal_types.filter(function(obj) {
              return obj.value === $scope.shareholder.user.userprofile.legal_type;
            });
            $scope.shareholder.user.userprofile.legal_type = legal_type[0];
          }
          if ($scope.shareholder.user.userprofile.language) {
            language = $scope.languages.filter(function(obj) {
              return obj.iso === $scope.shareholder.user.userprofile.language;
            });
            return $scope.shareholder.user.userprofile.language = language[0];
          }
        }).then(function() {
          return void 0;
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          $scope.errors = rejection.data;
          return Raven.captureMessage('edit shareholder form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.datepicker = {
        opened: false
      };
      $scope.datepicker.format = 'd.MM.yy';
      $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      return $scope.open_datepicker = function() {
        return $scope.datepicker.opened = true;
      };
    }
  ]);

  app.filter('percentage', [
    '$filter', function($filter) {
      return function(input, decimals) {
        return $filter('number')(input * 100, decimals) + '%';
      };
    }
  ]);

  app.run(function(editableOptions) {
    editableOptions.theme = 'bs3';
  });

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.start', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('StartController', [
    '$scope', '$window', '$http', 'CompanyAdd', 'Shareholder', 'User', 'Company', '$timeout', function($scope, $window, $http, CompanyAdd, Shareholder, User, Company, $timeout) {
      $scope.shareholders = [];
      $scope.option_holders = [];
      $scope.user = [];
      $scope.total_shares = 0;
      $scope.loading = true;
      $scope.shareholder_added_success = false;
      $scope.next = false;
      $scope.previous = false;
      $scope.total = 0;
      $scope.current = 0;
      $scope.current_range = '';
      $scope.search_params = {
        'query': null,
        'ordering': null,
        'ordering_reverse': null
      };
      $scope.ordering_options = [
        {
          'name': gettext('Email'),
          'value': 'user__email'
        }, {
          'name': gettext('Shareholder Number'),
          'value': 'number'
        }, {
          'name': gettext('Last Name'),
          'value': 'user__last_name'
        }
      ];
      $scope.optionholder_next = false;
      $scope.optionholder_previous = false;
      $scope.optionholder_total = 0;
      $scope.optionholder_current = 0;
      $scope.optionholder_current_range = '';
      $scope.optionholder_search_params = {
        'query': null,
        'ordering': null,
        'ordering_reverse': null
      };
      $scope.optionholder_ordering_options = [
        {
          'name': gettext('Email'),
          'value': 'user__email'
        }, {
          'name': gettext('Shareholder Number'),
          'value': 'number'
        }, {
          'name': gettext('Last Name'),
          'value': 'user__last_name'
        }
      ];
      $scope.show_add_shareholder = false;
      $scope.newShareholder = new Shareholder();
      $scope.newCompany = new CompanyAdd();
      $scope.reset_search_params = function() {
        $scope.current = null;
        $scope.previous = null;
        $scope.next = null;
        return $scope.shareholders = [];
      };
      $scope.optionholder_reset_search_params = function() {
        $scope.optionholder_current = null;
        $scope.optionholder_previous = null;
        $scope.optionholder_next = null;
        return $scope.option_holders = [];
      };
      $scope.load_option_holders = function() {
        return $http.get('/services/rest/shareholders/option_holder').then(function(result) {
          angular.forEach(result.data.results, function(item) {
            return $scope.option_holders.push(item);
          });
          if (result.data.next) {
            $scope.optionholder_next = result.data.next;
          }
          if (result.data.previous) {
            $scope.optionholder_previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.optionholder_total = result.data.count;
          }
          if (result.data.current) {
            return $scope.optionholder_current = result.data.current;
          }
        });
      };
      $scope.load_all_shareholders = function() {
        $scope.reset_search_params();
        $scope.search_params.query = null;
        return $http.get('/services/rest/shareholders').then(function(result) {
          angular.forEach(result.data.results, function(item) {
            return $scope.shareholders.push(item);
          });
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            return $scope.current = result.data.current;
          }
        });
      };
      $scope.load_user = function() {
        return $http.get('/services/rest/user').then(function(result) {
          $scope.loading = true;
          $scope.user = result.data.results[0];
          return $http.get($scope.user.selected_company).then(function(result1) {
            return $scope.company = result1.data;
          });
        })["finally"](function() {
          return $scope.loading = false;
        });
      };
      $scope.load_all_shareholders();
      $scope.load_option_holders();
      $scope.load_user();
      $scope.$watchCollection('shareholders', function(shareholders) {
        $scope.total_shares = 0;
        return angular.forEach(shareholders, function(item) {
          return $scope.total_shares = item.share_count + $scope.total_shares;
        });
      });
      $scope.$watchCollection('current', function(current) {
        var end, start;
        start = ($scope.current - 1) * 20;
        end = Math.min($scope.current * 20, $scope.total);
        return $scope.current_range = start.toString() + '-' + end.toString();
      });
      $scope.$watchCollection('optionholder_current', function(optionholder_current) {
        var end, start;
        start = ($scope.optionholder_current - 1) * 20;
        end = Math.min($scope.optionholder_current * 20, $scope.optionholder_total);
        return $scope.optionholder_current_range = start.toString() + '-' + end.toString();
      });
      $scope.next_page = function() {
        if ($scope.next) {
          return $http.get($scope.next).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.shareholders.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.previous_page = function() {
        if ($scope.previous) {
          return $http.get($scope.previous).then(function(result) {
            $scope.reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.shareholders.push(item);
            });
            if (result.data.next) {
              $scope.next = result.data.next;
            } else {
              $scope.next = false;
            }
            if (result.data.previous) {
              $scope.previous = result.data.previous;
            } else {
              $scope.previous = false;
            }
            if (result.data.count) {
              $scope.total = result.data.count;
            }
            if (result.data.current) {
              return $scope.current = result.data.current;
            }
          });
        }
      };
      $scope.optionholder_next_page = function() {
        if ($scope.optionholder_next) {
          return $http.get($scope.optionholder_next).then(function(result) {
            $scope.optionholder_reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.option_holders.push(item);
            });
            if (result.data.next) {
              $scope.optionholder_next = result.data.next;
            } else {
              $scope.optionholder_next = false;
            }
            if (result.data.previous) {
              $scope.optionholder_previous = result.data.previous;
            } else {
              $scope.optionholder_previous = false;
            }
            if (result.data.count) {
              $scope.optionholder_total = result.data.count;
            }
            if (result.data.current) {
              return $scope.optionholder_current = result.data.current;
            }
          });
        }
      };
      $scope.optionholder_previous_page = function() {
        if ($scope.optionholder_previous) {
          return $http.get($scope.optionholder_previous).then(function(result) {
            $scope.optionholder_reset_search_params();
            angular.forEach(result.data.results, function(item) {
              return $scope.option_holders.push(item);
            });
            if (result.data.next) {
              $scope.optionholder_next = result.data.next;
            } else {
              $scope.optionholder_next = false;
            }
            if (result.data.previous) {
              $scope.optionholder_previous = result.data.previous;
            } else {
              $scope.optionholder_previous = false;
            }
            if (result.data.count) {
              $scope.optionholder_total = result.data.count;
            }
            if (result.data.current) {
              return $scope.optionholder_current = result.data.current;
            }
          });
        }
      };
      $scope.search = function() {
        var params, paramss;
        params = {};
        if ($scope.search_params.query) {
          params.search = $scope.search_params.query;
        }
        if ($scope.search_params.ordering) {
          params.ordering = $scope.search_params.ordering;
        }
        paramss = $.param(params);
        return $http.get('/services/rest/shareholders?' + paramss).then(function(result) {
          $scope.reset_search_params();
          angular.forEach(result.data.results, function(item) {
            return $scope.shareholders.push(item);
          });
          if (result.data.next) {
            $scope.next = result.data.next;
          }
          if (result.data.previous) {
            $scope.previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.total = result.data.count;
          }
          if (result.data.current) {
            $scope.current = result.data.current;
          }
          return $scope.search_params.query = params.search;
        });
      };
      $scope.optionholder_search = function() {
        var params, paramss;
        params = {};
        params.company = $scope.company;
        if ($scope.optionholder_search_params.query) {
          params.search = $scope.optionholder_search_params.query;
        }
        if ($scope.optionholder_search_params.ordering) {
          params.ordering = $scope.optionholder_search_params.ordering;
        }
        paramss = $.param(params);
        return $http.get('/services/rest/shareholders/option_holder?' + paramss).then(function(result) {
          $scope.optionholder_reset_search_params();
          angular.forEach(result.data.results, function(item) {
            return $scope.option_holders.push(item);
          });
          if (result.data.next) {
            $scope.optionholder_next = result.data.next;
          }
          if (result.data.previous) {
            $scope.optionholder_previous = result.data.previous;
          }
          if (result.data.count) {
            $scope.optionholder_total = result.data.count;
          }
          if (result.data.current) {
            $scope.optionholder_current = result.data.current;
          }
          return $scope.optionholder_search_params.query = params.search;
        });
      };
      $scope.add_company = function() {
        $scope.errors = null;
        return $scope.newCompany.$save().then(function(result) {
          $scope.load_user();
          return $scope.load_all_shareholders();
        }).then(function() {
          $scope.newCompany = new Company();
          return $window.ga('send', 'event', 'form-send', 'add-company');
        }).then(function() {
          return $scope.errors = null;
        }, function(rejection) {
          $scope.errors = rejection.data;
          return Raven.captureMessage('add corp form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.add_shareholder = function() {
        $scope.errors = null;
        return $scope.newShareholder.$save().then(function(result) {
          return $scope.shareholders.push(result);
        }).then(function() {
          $scope.newShareholder = new Shareholder();
          $scope.shareholder_added_success = true;
          $scope.show_add_shareholder = false;
          return $timeout(function() {
            return $scope.shareholder_added_success = false;
          }, 30000);
        }).then(function() {
          $scope.errors = null;
          return $window.ga('send', 'event', 'form-send', 'add-shareholder');
        }, function(rejection) {
          $scope.errors = rejection.data;
          return Raven.captureMessage('add shareholder form error: ' + rejection.statusText, {
            level: 'warning',
            extra: {
              rejection: rejection
            }
          });
        });
      };
      $scope.show_add_shareholder_form = function() {
        return $scope.show_add_shareholder = true;
      };
      $scope.hide_form = function() {
        return $scope.show_add_shareholder = false;
      };
      $scope.goto_shareholder = function(shareholder_id) {
        return window.location = "/shareholder/" + shareholder_id + "/";
      };
      $scope.datepicker = {
        opened: false
      };
      $scope.datepicker.format = 'd. MMM yyyy';
      $scope.datepicker.options = {
        formatYear: 'yy',
        startingDay: 1,
        showWeeks: false
      };
      return $scope.toggle_datepicker = function() {
        $scope.datepicker.opened = !$scope.datepicker.opened;
        return false;
      };
    }
  ]);

}).call(this);

(function() {
  var app;

  app = angular.module('js.darg.app.tfa', ['js.darg.api', 'pascalprecht.translate', 'ui.bootstrap']);

  app.config([
    '$translateProvider', function($translateProvider) {
      $translateProvider.translations('de', django.catalog);
      $translateProvider.preferredLanguage('de');
      return $translateProvider.useSanitizeValueStrategy('escaped');
    }
  ]);

  app.controller('TwoFactorAuthenticationController', [
    '$scope', '$http', '$window', '$filter', function($scope, $http, $window, $filter) {
      return $scope.submit = function() {
        $('form')[0].submit();
        return console.log('f');
      };
    }
  ]);

}).call(this);
