# Наводим порядок

Прежде чем мы начнем собирать воедино паззл из полученных знаний в осмысленное приложение, предлагаю сразу раскидать стили и верстку, так как они не являются темами для обсуждения в подробностях.

## Стили

Обычно файл со стилями кладут в то же место, где находится и компонент. У нас же для простоты - все стили будут храниться в `index.css`

_src/index.css_

```css
/* http://meyerweb.com/eric/tools/css/reset/
   v2.0 | 20110126
   License: none (public domain)
*/

html,
body,
div,
span,
applet,
object,
iframe,
h1,
h2,
h3,
h4,
h5,
h6,
p,
blockquote,
pre,
a,
abbr,
acronym,
address,
big,
cite,
code,
del,
dfn,
em,
img,
ins,
kbd,
q,
s,
samp,
small,
strike,
strong,
sub,
sup,
tt,
var,
b,
u,
i,
center,
dl,
dt,
dd,
ol,
ul,
li,
fieldset,
form,
label,
legend,
table,
caption,
tbody,
tfoot,
thead,
tr,
th,
td,
article,
aside,
canvas,
details,
embed,
figure,
figcaption,
footer,
header,
hgroup,
menu,
nav,
output,
ruby,
section,
summary,
time,
mark,
audio,
video {
  margin: 0;
  padding: 0;
  border: 0;
  font-size: 100%;
  font: inherit;
  vertical-align: baseline;
}
/* HTML5 display-role reset for older browsers */
article,
aside,
details,
figcaption,
figure,
footer,
header,
hgroup,
menu,
nav,
section {
  display: block;
}
body {
  line-height: 1;
  font-family: sans-serif;
}
ol,
ul {
  list-style: none;
}
blockquote,
q {
  quotes: none;
}
blockquote:before,
blockquote:after,
q:before,
q:after {
  content: '';
  content: none;
}
table {
  border-collapse: collapse;
  border-spacing: 0;
}

/*end reset*/

h3 {
  font-size: 22px;
  margin: 10px 0 0;
}
.app {
  margin: 50px;
  font: 14px sans-serif;
}
.ib {
  display: inline-block;
}
.page {
  width: 80%;
}
.user {
  width: 20%;
  vertical-align: top;
}

.btn {
  border: none;
  border-radius: 2px;
  display: inline-block;
  height: 36px;
  line-height: 36px;
  font-size: 16px;
  outline: 0;
  padding: 0 2rem;
  text-transform: uppercase;
  vertical-align: middle;
  color: #fff;
  background-color: #6383a8;
  text-align: center;
  letter-spacing: 0.5px;
  transition: 0.2s ease-out;
  cursor: pointer;
}
.btn:hover {
  background-color: #6d8cb0;
}
```

Так же, очень популярен подход с использованием [styled-components](https://www.styled-components.com/)

Во многих проектах, вы можете встретить библиотеку [classnames](https://github.com/JedWatson/classnames) для организации стилей по условию.

## Верстка

Здесь двояко: с одной стороны, верстка в реакте та же самая, с другой стороны - верстальщик, который понимает как работает react, стряпает компоненты гораздо чище (старается держать все компоненты "тупыми" и может сам написать простые условия).

Для нашего приложения измененная верстка и стили дадут следующий эффект:

![Разметка](new-css-html.jpg)

Наконец-то наше приложение стало похоже на схему :)

Так как вопросы верстки и стилей не являются темой нашего обучения, вы можете скопировать исходный код, либо сделать как вам хочется.

Напоминаю: в реальном приложении, лучше держать стили рядом с компонентом, чтобы можно было удобно переиспользовать компоненты между приложениями.

Итого: наше приложение похоже на схему. Автор выдал несколько ссылок на организацию CSS и смылся.

[Исходный код](https://github.com/maxfarseer/redux-course-ru-v2/tree/chp9-new-css-html-cleanup).
