# Стилизация и CSS

## Как добавить CSS-классы в компоненты? {#how-do-i-add-css-classes-to-components}

Передайте в проп `className` строку:

```js
render() {
  return <span className="menu navigation-menu">Меню</span>
}
```

Обычно CSS-классы зависят от пропсов или состояния:

```js
render() {
  let className = 'menu';
  if (this.props.isActive) {
    className += ' menu-active';
  }
  return <span className={className}>Меню</span>
}
```

> Совет
>
> Если вы часто пишите похожий код, то пакет [classnames](https://www.npmjs.com/package/classnames#usage-with-reactjs) поможет упростить его.

## Встроенные стили — это плохо? {#are-inline-styles-bad}

CSS-классы, как правило, лучше для производительности, чем встроенные стили.

## Что такое CSS-in-JS? {#what-is-css-in-js}

«CSS-in-JS» — это паттерн, в котором CSS-код создаётся при помощи JavaScript, вместо того, чтобы писать его во внешних файлах. Ознакомьтесь со сравнением библиотек по работе с «CSS-in-JS» в [этом репозитории](https://github.com/MicheleBertoli/css-in-js).

_Обратите внимание, что данная функциональность не входит в React из коробки, а предоставляется сторонними библиотеками._ React ничего не знает про то, как определяются стили. Если вы сомневаетесь, использовать указанный выше способ, то хорошим началом станет определение стилей в отдельном файле с расширением `*.css`, как вы ранее привыкли это делать, а затем указать нужные классы с помощью `className`.

### Можно создавать анимации в React? {#can-i-do-animations-in-react}

React может использоваться для создания крутых анимаций! В качестве примера посмотрите библиотеки [React Transition Group](https://reactcommunity.org/react-transition-group/) и [React Motion](https://github.com/chenglou/react-motion).
