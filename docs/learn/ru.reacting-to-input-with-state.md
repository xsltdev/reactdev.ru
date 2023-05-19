React предоставляет декларативный способ манипулирования пользовательским интерфейсом. Вместо того чтобы напрямую управлять отдельными частями пользовательского интерфейса, вы описываете различные состояния, в которых может находиться ваш компонент, и переключаетесь между ними в ответ на ввод пользователя. Это похоже на то, как дизайнеры думают о пользовательском интерфейсе.


  - Чем декларативное программирование пользовательского интерфейса отличается от императивного программирования пользовательского интерфейса
  - Как перечислить различные визуальные состояния, в которых может находиться ваш компонент
  - Как вызвать изменения между различными визуальными состояниями из кода


## Как декларативный пользовательский интерфейс отличается от императивного {/*how-declarative-ui-compares-to-imperative*/}


Когда вы проектируете взаимодействие пользовательского интерфейса, вы, вероятно, думаете о том, как пользовательский интерфейс *изменяется* в ответ на действия пользователя. Рассмотрим форму, которая позволяет пользователю отправить ответ:


  - Когда вы вводите что-то в форму, кнопка "Отправить" ** становится активной*.
  - Когда вы нажимаете кнопку "Отправить", и форма, и кнопка **отключаются,** и появляется волчок **.
  - Если сетевой запрос прошел успешно, форма **спрячется,** и появится сообщение "Спасибо "**.
  - Если сетевой запрос не удался, появляется сообщение об ошибке **, ** и форма снова становится открытой**.


В **императивном программировании** вышесказанное прямо соответствует тому, как вы реализуете взаимодействие. Вы должны написать точные инструкции для манипулирования пользовательским интерфейсом в зависимости от того, что только что произошло. Вот еще один способ подумать об этом: представьте, что вы едете рядом с кем-то в машине и говорите ему пошагово, куда ехать.


\<Illustration src="/images/docs/illustrations/i\_imperative-ui-programming.png" alt="В машине, управляемой озабоченным человеком, представляющим JavaScript, пассажир приказывает водителю выполнить последовательность сложных поворотов." /\>


Они не знают, куда вы хотите поехать, они просто следуют вашим командам. (И если вы ошибетесь в указаниях, вы окажетесь не в том месте\!) Это называется *императивным*, потому что вы должны "командовать" каждым элементом, от спиннера до кнопки, указывая компьютеру *как* обновить пользовательский интерфейс.


В этом примере императивного программирования пользовательского интерфейса форма построена *без* React. Она использует только браузерный [DOM] (https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model):


<!-- 0001.part.md -->


``` js
async function handleFormSubmit(e) {
  e.preventDefault();
  disable(textarea);
  disable(button);
  show(loadingMessage);
  hide(errorMessage);
  try {
    await submitForm(textarea.value);
    show(successMessage);
    hide(form);
  } catch (err) {
    show(errorMessage);
    errorMessage.textContent = err.message;
  } finally {
    hide(loadingMessage);
    enable(textarea);
    enable(button);
  }
}

function handleTextareaChange() {
  if (textarea.value.length === 0) {
    disable(button);
  } else {
    enable(button);
  }
}

function hide(el) {
  el.style.display = 'none';
}

function show(el) {
  el.style.display = '';
}

function enable(el) {
  el.disabled = false;
}

function disable(el) {
  el.disabled = true;
}

function submitForm(answer) {
  // Pretend it's hitting the network.
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if (answer.toLowerCase() == 'istanbul') {
        resolve();
      } else {
        reject(new Error('Good guess but a wrong answer. Try again!'));
      }
    }, 1500);
  });
}

let form = document.getElementById('form');
let textarea = document.getElementById('textarea');
let button = document.getElementById('button');
let loadingMessage = document.getElementById('loading');
let errorMessage = document.getElementById('error');
let successMessage = document.getElementById('success');
form.onsubmit = handleFormSubmit;
textarea.oninput = handleTextareaChange;
```


<!-- 0002.part.md -->




<!-- 0003.part.md -->


``` js
{
  "hardReloadOnChange": true
}
```


<!-- 0004.part.md -->




\`\`\`html public/index.html \<form id=“form”\> \<h2\>City quiz\</h2\> \<p\> What city is located on two continents? \</p\> \<textarea id=“textarea”\>\</textarea\> \<br /\> \<button id=“button” disabled\>Submit\</button\> \<p id=“loading” style=“display: none”\>Loading…\</p\> \<p id=“error” style=“display: none; color: red;”\>\</p\> \</form\> \<h1 id=“success” style=“display: none”\>That’s right\!\</h1\>


\<style\> \* { box-sizing: border-box; } body { font-family: sans-serif; margin: 20px; padding: 0; } \</style\>


<!-- 0005.part.md -->


```` 


Manipulating the UI imperatively works well enough for isolated examples, but it gets exponentially more difficult to manage in more complex systems. Imagine updating a page full of different forms like this one. Adding a new UI element or a new interaction would require carefully checking all existing code to make sure you haven't introduced a bug (for example, forgetting to show or hide something).

React was built to solve this problem.

In React, you don't directly manipulate the UI--meaning you don't enable, disable, show, or hide components directly. Instead, you **declare what you want to show,** and React figures out how to update the UI. Think of getting into a taxi and telling the driver where you want to go instead of telling them exactly where to turn. It's the driver's job to get you there, and they might even know some shortcuts you haven't considered!

<Illustration src="/images/docs/illustrations/i_declarative-ui-programming.png" alt="In a car driven by React, a passenger asks to be taken to a specific place on the map. React figures out how to do that." />

## Thinking about UI declaratively {/*thinking-about-ui-declaratively*/}

You've seen how to implement a form imperatively above. To better understand how to think in React, you'll walk through reimplementing this UI in React below:

1. **Identify** your component's different visual states
2. **Determine** what triggers those state changes
3. **Represent** the state in memory using `useState`
4. **Remove** any non-essential state variables
5. **Connect** the event handlers to set the state

### Step 1: Identify your component's different visual states {/*step-1-identify-your-components-different-visual-states*/}

In computer science, you may hear about a ["state machine"](https://en.wikipedia.org/wiki/Finite-state_machine) being in one of several “states”. If you work with a designer, you may have seen mockups for different "visual states". React stands at the intersection of design and computer science, so both of these ideas are sources of inspiration.

First, you need to visualize all the different "states" of the UI the user might see:

* **Empty**: Form has a disabled "Submit" button.
* **Typing**: Form has an enabled "Submit" button.
* **Submitting**: Form is completely disabled. Spinner is shown.
* **Success**: "Thank you" message is shown instead of a form.
* **Error**: Same as Typing state, but with an extra error message.

Just like a designer, you'll want to "mock up" or create "mocks" for the different states before you add logic. For example, here is a mock for just the visual part of the form. This mock is controlled by a prop called `status` with a default value of `'empty'`:


```js


<!-- 0006.part.md -->


export default function Form({
  status = 'empty'
}) {
  if (status === 'success') {
    return <h1>That's right!</h1>
  }
  return (
    <>
      <h2>City quiz</h2>
      <p>
        In which city is there a billboard that turns air into drinkable water?
      </p>
      <form>
        <textarea />
        <br />
        <button>
          Submit
        </button>
      </form>
    </>
  )
}


<!-- 0007.part.md -->


````

You could call that prop anything you like, the naming is not important. Try editing `status = 'empty'` to `status = 'success'` to see the success message appear. Mocking lets you quickly iterate on the UI before you wire up any logic. Here is a more fleshed out prototype of the same component, still “controlled” by the `status` prop:

``` js


<!-- 0008.part.md -->


export default function Form({
  // Try 'submitting', 'error', 'success':
  status = 'empty'
}) {
  if (status === 'success') {
    return <h1>That's right!</h1>
  }
  return (
    <>
      <h2>City quiz</h2>
      <p>
        In which city is there a billboard that turns air into drinkable water?
      </p>
      <form>
        <textarea disabled={
          status === 'submitting'
        } />
        <br />
        <button disabled={
          status === 'empty' ||
          status === 'submitting'
        }>
          Submit
        </button>
        {status === 'error' &&
          <p className="Error">
            Good guess but a wrong answer. Try again!
          </p>
        }
      </form>
      </>
  );
}


<!-- 0009.part.md -->


```

``` css


<!-- 0010.part.md -->


.Error { цвет: красный; }


<!-- 0011.part.md -->


```

#### Displaying many visual states at once {/*displaying-many-visual-states-at-once*/}

If a component has a lot of visual states, it can be convenient to show them all on one page:

``` js


<!-- 0012.part.md -->


import Form from './Form.js';


let statuses = [
  'empty',
  'typing',
  'submitting',
  'success',
  'error',
];


export default function App() {
  return (
    <>
      {statuses.map(status => (
        <section key={status}>
          <h4>Форма ({status}):</h4>
          <Form status={status} />
        </section>
      ))}
    </>
  );
}


<!-- 0013.part.md -->


```

``` js


<!-- 0014.part.md -->


export default function Form({ status }) {
  if (status === 'success') {
    return <h1>That's right!</h1>
  }
  return (
    <form>
      <textarea disabled={
        status === 'submitting'
      } />
      <br />
      <button disabled={
        status === 'empty' ||
        status === 'submitting'
      }>
        Submit
      </button>
      {status === 'error' &&
        <p className="Error">
          Good guess but a wrong answer. Try again!
        </p>
      }
    </form>
  );
}


<!-- 0015.part.md -->


```

``` css


<!-- 0016.part.md -->


section { border-bottom: 1px solid #aaa; padding: 20px; }
h4 { color: #222; }
body { margin: 0; }
.Error { цвет: красный; }


<!-- 0017.part.md -->


```

Pages like this are often called “living styleguides” or “storybooks”.

### Step 2: Determine what triggers those state changes {/*step-2-determine-what-triggers-those-state-changes*/}

You can trigger state updates in response to two kinds of inputs:

  - **Human inputs,** like clicking a button, typing in a field, navigating a link.
  - **Computer inputs,** like a network response arriving, a timeout completing, an image loading.

\<IllustrationBlock\> \<Illustration caption=“Human inputs” alt=“A finger.” src=“/images/docs/illustrations/i\_inputs1.png” /\> \<Illustration caption=“Computer inputs” alt=“Ones and zeroes.” src=“/images/docs/illustrations/i\_inputs2.png” /\> \</IllustrationBlock\>

In both cases, **you must set [state variables](/learn/state-a-components-memory#anatomy-of-usestate) to update the UI.** For the form you’re developing, you will need to change state in response to a few different inputs:

  - **Changing the text input** (human) should switch it from the *Empty* state to the *Typing* state or back, depending on whether the text box is empty or not.
  - **Clicking the Submit button** (human) should switch it to the *Submitting* state.
  - **Successful network response** (computer) should switch it to the *Success* state.
  - **Failed network response** (computer) should switch it to the *Error* state with the matching error message.

Notice that human inputs often require [event handlers](/learn/responding-to-events)\!

To help visualize this flow, try drawing each state on paper as a labeled circle, and each change between two states as an arrow. You can sketch out many flows this way and sort out bugs long before implementation.

\<DiagramGroup\>

\<Diagram name=“responding\_to\_input\_flow” height={350} width={688} alt=“Flow chart moving left to right with 5 nodes. The first node labeled ‘empty’ has one edge labeled ‘start typing’ connected to a node labeled ‘typing’. That node has one edge labeled ‘press submit’ connected to a node labeled ‘submitting’, which has two edges. The left edge is labeled ‘network error’ connecting to a node labeled ‘error’. The right edge is labeled ‘network success’ connecting to a node labeled ‘success’.”\>

Form states

\</Diagram\>

\</DiagramGroup\>

### Step 3: Represent the state in memory with `useState` {/*step-3-represent-the-state-in-memory-with-usestate*/}

Next you’ll need to represent the visual states of your component in memory with [`useState`.](/reference/react/useState) Simplicity is key: each piece of state is a “moving piece”, and **you want as few “moving pieces” as possible.** More complexity leads to more bugs\!

Start with the state that *absolutely must* be there. For example, you’ll need to store the `answer` for the input, and the `error` (if it exists) to store the last error:

``` js


<!-- 0018.part.md -->


const [answer, setAnswer] = useState('');
const [error, setError] = useState(null);


<!-- 0019.part.md -->


```

Then, you’ll need a state variable representing which one of the visual states that you want to display. There’s usually more than a single way to represent that in memory, so you’ll need to experiment with it.

If you struggle to think of the best way immediately, start by adding enough state that you’re *definitely* sure that all the possible visual states are covered:

``` js


<!-- 0020.part.md -->


const [isEmpty, setIsEmpty] = useState(true);
const [isTyping, setIsTyping] = useState(false);
const [isSubmitting, setIsSubmitting] = useState(false);
const [isSuccess, setIsSuccess] = useState(false);
const [isError, setIsError] = useState(false);


<!-- 0021.part.md -->


```

Your first idea likely won’t be the best, but that’s ok–refactoring state is a part of the process\!

### Step 4: Remove any non-essential state variables {/*step-4-remove-any-non-essential-state-variables*/}

You want to avoid duplication in the state content so you’re only tracking what is essential. Spending a little time on refactoring your state structure will make your components easier to understand, reduce duplication, and avoid unintended meanings. Your goal is to **prevent the cases where the state in memory doesn’t represent any valid UI that you’d want a user to see.** (For example, you never want to show an error message and disable the input at the same time, or the user won’t be able to correct the error\!)

Here are some questions you can ask about your state variables:

  - **Does this state cause a paradox?** For example, `isTyping` and `isSubmitting` can’t both be `true`. A paradox usually means that the state is not constrained enough. There are four possible combinations of two booleans, but only three correspond to valid states. To remove the “impossible” state, you can combine these into a `status` that must be one of three values: `'typing'`, `'submitting'`, or `'success'`.
  - **Is the same information available in another state variable already?** Another paradox: `isEmpty` and `isTyping` can’t be `true` at the same time. By making them separate state variables, you risk them going out of sync and causing bugs. Fortunately, you can remove `isEmpty` and instead check `answer.length === 0`.
  - **Can you get the same information from the inverse of another state variable?** `isError` is not needed because you can check `error !== null` instead.

After this clean-up, you’re left with 3 (down from 7\!) *essential* state variables:

``` js


<!-- 0022.part.md -->


const [answer, setAnswer] = useState('');
const [error, setError] = useState(null);
const [status, setStatus] = useState('typing'); // 'typing', 'submitting', or 'success'


<!-- 0023.part.md -->


```

You know they are essential, because you can’t remove any of them without breaking the functionality.

#### Eliminating “impossible” states with a reducer {/*eliminating-impossible-states-with-a-reducer*/}

These three variables are a good enough representation of this form’s state. However, there are still some intermediate states that don’t fully make sense. For example, a non-null `error` doesn’t make sense when `status` is `'success'`. To model the state more precisely, you can [extract it into a reducer.](/learn/extracting-state-logic-into-a-reducer) Reducers let you unify multiple state variables into a single object and consolidate all the related logic\!

### Step 5: Connect the event handlers to set state {/*step-5-connect-the-event-handlers-to-set-state*/}

Lastly, create event handlers that update the state. Below is the final form, with all event handlers wired up:

``` js


<!-- 0024.part.md -->


import { useState } from 'react';


export default function Form() {
  const [answer, setAnswer] = useState('');
  const [error, setError] = useState(null);
  const [status, setStatus] = useState('typing');


  if (status === 'success') {
    return <h1>Это правильно!</h1>
  }


  async function handleSubmit(e) {
    e.preventDefault();
    setStatus('submitting');
    try {
      await submitForm(answer);
      setStatus('success');
    } catch (err) {
      setStatus('ввод');
      setError(err);
    }
  }


  function handleTextareaChange(e) {
    setAnswer(e.target.value);
  }


  return (
    <>
      <h2>Городская викторина</h2>
      <p>
        В каком городе есть рекламный щит, который превращает воздух в питьевую воду?
      </p>
      <form onSubmit={handleSubmit}>
        <textarea
          value={ответ}
          onChange={handleTextareaChange}
          disabled={status === 'submitting'}
        />
        <br />
        <button disabled={
          answer.length === 0 ||
          status === 'submitting'
        }>
          Submit
        </button>
        {error !== null &&
          <p className="Error">
            {error.message}
          </p>
        }
      </form>
    </>
  );
}


function submitForm(answer) {
  // Pretend it's hitting the network.
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      let shouldError = answer.toLowerCase() !== 'lima'
      if (shouldError) {
        reject(new Error('Good guess but a wrong answer. Try again!'));
      } else {
        resolve();
      }
    }, 1500);
  });
}


<!-- 0025.part.md -->


```

``` css


<!-- 0026.part.md -->


.Error { цвет: красный; }


<!-- 0027.part.md -->


```

Although this code is longer than the original imperative example, it is much less fragile. Expressing all interactions as state changes lets you later introduce new visual states without breaking existing ones. It also lets you change what should be displayed in each state without changing the logic of the interaction itself.

\<Recap\>

  - Declarative programming means describing the UI for each visual state rather than micromanaging the UI (imperative).
  - When developing a component:
    1.  Identify all its visual states.
    2.  Determine the human and computer triggers for state changes.
    3.  Model the state with `useState`.
    4.  Remove non-essential state to avoid bugs and paradoxes.
    5.  Connect the event handlers to set state.

\</Recap\>

\<Challenges\>

#### Add and remove a CSS class {/*add-and-remove-a-css-class*/}

Make it so that clicking on the picture *removes* the `background--active` CSS class from the outer `<div>`, but *adds* the `picture--active` class to the `<img>`. Clicking the background again should restore the original CSS classes.

Visually, you should expect that clicking on the picture removes the purple background and highlights the picture border. Clicking outside the picture highlights the background, but removes the picture border highlight.

``` js


<!-- 0028.part.md -->


export default function Picture() {
  return (
    <div className="background background--active">
      <img
        className="picture"
        alt="Rainbow houses in Kampung Pelangi, Indonesia"
        src="https://i.imgur.com/5qwVYb1.jpeg"
      />
    </div>
  );
}


<!-- 0029.part.md -->


```

``` css


<!-- 0030.part.md -->


body { margin: 0; padding: 0; высота: 250px; }


.background {
  ширина: 100vw;
  высота: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #eee;
}


.background--active {
  фон: #a6b5ff;
}


.picture {
  ширина: 200px;
  высота: 200px;
  border-radius: 10px;
}


.picture--active {
  border: 5px solid #a6b5ff;
}


<!-- 0031.part.md -->


```

\<Solution\>

This component has two visual states: when the image is active, and when the image is inactive:

  - When the image is active, the CSS classes are `background` and `picture picture--active`.
  - When the image is inactive, the CSS classes are `background background--active` and `picture`.

A single boolean state variable is enough to remember whether the image is active. The original task was to remove or add CSS classes. However, in React you need to *describe* what you want to see rather than *manipulate* the UI elements. So you need to calculate both CSS classes based on the current state. You also need to [stop the propagation](/learn/responding-to-events#stopping-propagation) so that clicking the image doesn’t register as a click on the background.

Verify that this version works by clicking the image and then outside of it:

``` js


<!-- 0032.part.md -->


import { useState } from 'react';


export default function Picture() {
  const [isActive, setIsActive] = useState(false);


  let backgroundClassName = 'background';
  let pictureClassName = 'picture';
  if (isActive) {
    pictureClassName += ' picture--active';
  } else {
    backgroundClassName += ' background--active';
  }


  return (
    <div
      className={backgroundClassName}
      onClick={() => setIsActive(false)}
    >
      <img
        onClick={e => {
          e.stopPropagation();
          setIsActive(true);
        }}
        className={pictureClassName}
        alt="Rainbow houses in Kampung Pelangi, Indonesia"
        src="https://i.imgur.com/5qwVYb1.jpeg"
      />
    </div>
  );
}


<!-- 0033.part.md -->


```

``` css


<!-- 0034.part.md -->


body { margin: 0; padding: 0; высота: 250px; }


.background {
  ширина: 100vw;
  высота: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #eee;
}


.background--active {
  фон: #a6b5ff;
}


.picture {
  ширина: 200px;
  высота: 200px;
  border-radius: 10px;
  border: 5px solid transparent;
}


.picture--active {
  border: 5px solid #a6b5ff;
}


<!-- 0035.part.md -->


```

Alternatively, you could return two separate chunks of JSX:

``` js


<!-- 0036.part.md -->


import { useState } from 'react';


export default function Picture() {
  const [isActive, setIsActive] = useState(false);
  if (isActive) {
    return (
      <div
        className="background"
        onClick={() => setIsActive(false)}
      >
        <img
          className="picture picture--active"
          alt="Rainbow houses in Kampung Pelangi, Indonesia"
          src="https://i.imgur.com/5qwVYb1.jpeg"
          onClick={e => e.stopPropagation()}
        />
      </div>
    );
  }
  return (
    <div className="background background--active">
      <img
        className="picture"
        alt="Rainbow houses in Kampung Pelangi, Indonesia"
        src="https://i.imgur.com/5qwVYb1.jpeg"
        onClick={() => setIsActive(true)}
      />
    </div>
  );
}


<!-- 0037.part.md -->


```

``` css


<!-- 0038.part.md -->


body { margin: 0; padding: 0; высота: 250px; }


.background {
  ширина: 100vw;
  высота: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #eee;
}


.background--active {
  фон: #a6b5ff;
}


.picture {
  ширина: 200px;
  высота: 200px;
  border-radius: 10px;
  border: 5px solid transparent;
}


.picture--active {
  border: 5px solid #a6b5ff;
}


<!-- 0039.part.md -->


```

Keep in mind that if two different JSX chunks describe the same tree, their nesting (first `<div>` → first `<img>`) has to line up. Otherwise, toggling `isActive` would recreate the whole tree below and [reset its state.](/learn/preserving-and-resetting-state) This is why, if a similar JSX tree gets returned in both cases, it is better to write them as a single piece of JSX.

\</Solution\>

#### Profile editor {/*profile-editor*/}

Here is a small form implemented with plain JavaScript and DOM. Play with it to understand its behavior:

``` js


<!-- 0040.part.md -->


function handleFormSubmit(e) {
  e.preventDefault();
  if (editButton.textContent === 'Редактировать профиль') {
    editButton.textContent = 'Сохранить профиль';
    hide(firstNameText);
    hide(lastNameText);
    show(firstNameInput);
    show(lastNameInput);
  } else {
    editButton.textContent = 'Редактировать профиль';
    hide(firstNameInput);
    hide(lastNameInput);
    show(firstNameText);
    show(lastNameText);
  }
}


function handleFirstNameChange() {
  firstNameText.textContent = firstNameInput.value;
  helloText.textContent = (
    'Hello ' +
    firstNameInput.value + ' ' +
    lastNameInput.value + '!'
  );
}


function handleLastNameChange() {
  lastNameText.textContent = lastNameInput.value;
  helloText.textContent = (
    'Hello ' +
    firstNameInput.value + ' ' +
    lastNameInput.value + '!'
  );
}


function hide(el) {
  el.style.display = 'none';
}


function show(el) {
  el.style.display = '';
}


let form = document.getElementById('form');
let editButton = document.getElementById('editButton');
let firstNameInput = document.getElementById('firstNameInput');
let firstNameText = document.getElementById('firstNameText');
let lastNameInput = document.getElementById('lastNameInput');
let lastNameText = document.getElementById('lastNameText');
let helloText = document.getElementById('helloText');
form.onsubmit = handleFormSubmit;
firstNameInput.oninput = handleFirstNameChange;
lastNameInput.oninput = handleLastNameChange;


<!-- 0041.part.md -->


```

``` js


<!-- 0042.part.md -->


{
  "hardReloadOnChange": true
}


<!-- 0043.part.md -->


```

\`\`\`html public/index.html \<form id=“form”\> \<label\> First name: \<b id=“firstNameText”\>Jane\</b\> \<input id=“firstNameInput” value=“Jane” style=“display: none”\> \</label\> \<label\> Last name: \<b id=“lastNameText”\>Jacobs\</b\> \<input id=“lastNameInput” value=“Jacobs” style=“display: none”\> \</label\> \<button type=“submit” id=“editButton”\>Edit Profile\</button\> \<p\>\<i id=“helloText”\>Hello, Jane Jacobs\!\</i\>\</p\> \</form\>

\<style\> \* { box-sizing: border-box; } body { font-family: sans-serif; margin: 20px; padding: 0; } label { display: block; margin-bottom: 20px; } \</style\>

```` 


<!-- 0044.part.md -->





Эта форма переключается между двумя режимами: в режиме редактирования вы видите вводимые данные, а в режиме просмотра - только результат. Метка кнопки меняется между "Редактировать" и "Сохранить" в зависимости от того, в каком режиме вы находитесь. Когда вы изменяете вводимые данные, приветственное сообщение внизу обновляется в режиме реального времени.


Ваша задача - реализовать это на React в песочнице ниже. Для вашего удобства разметка уже была преобразована в JSX, но вам нужно будет сделать так, чтобы она показывала и скрывала входы, как это делает оригинал.


Убедитесь, что она также обновляет текст внизу!


<!-- 0045.part.md -->


```js
export default function EditProfile() {
  return (
    <form>
      <label>
        First name:{' '}
        <b>Jane</b>
        <input />
      </label>
      <label>
        Last name:{' '}
        <b>Jacobs</b>
        <input />
      </label>
      <button type="submit">
        Edit Profile
      </button>
      <p><i>Hello, Jane Jacobs!</i></p>
    </form>
  );
}
````


<!-- 0046.part.md -->




<!-- 0047.part.md -->


``` css
label { display: block; margin-bottom: 20px; }
```


<!-- 0048.part.md -->




\<Решение\>


Вам понадобятся две переменные состояния для хранения входных значений: `firstName` и `lastName`. Вам также понадобится переменная состояния `isEditing`, которая будет определять, отображать ли вводимые значения или нет. Вам *не* понадобится переменная `fullName`, потому что полное имя всегда может быть вычислено из `firstName` и `lastName`.


Наконец, вы должны использовать [условный рендеринг](/learn/conditional-rendering), чтобы показывать или скрывать входы в зависимости от `isEditing`.


<!-- 0049.part.md -->


``` js
import { useState } from 'react';

export default function EditProfile() {
  const [isEditing, setIsEditing] = useState(false);
  const [firstName, setFirstName] = useState('Jane');
  const [lastName, setLastName] = useState('Jacobs');

  return (
    <form onSubmit={e => {
      e.preventDefault();
      setIsEditing(!isEditing);
    }}>
      <label>
        First name:{' '}
        {isEditing ? (
          <input
            value={firstName}
            onChange={e => {
              setFirstName(e.target.value)
            }}
          />
        ) : (
          <b>{firstName}</b>
        )}
      </label>
      <label>
        Last name:{' '}
        {isEditing ? (
          <input
            value={lastName}
            onChange={e => {
              setLastName(e.target.value)
            }}
          />
        ) : (
          <b>{lastName}</b>
        )}
      </label>
      <button type="submit">
        {isEditing ? 'Save' : 'Edit'} Profile
      </button>
      <p><i>Hello, {firstName} {lastName}!</i></p>
    </form>
  );
}
```


<!-- 0050.part.md -->




<!-- 0051.part.md -->


``` css
label { display: block; margin-bottom: 20px; }
```


<!-- 0052.part.md -->




Сравните это решение с исходным императивным кодом. Чем они отличаются?


\</Solution\>


#### Рефакторинг императивного решения без React {/*refactor-the-imperative-solution-without-react*/}


Вот исходная песочница из предыдущей задачи, написанная императивно без React:


<!-- 0053.part.md -->


``` js
function handleFormSubmit(e) {
  e.preventDefault();
  if (editButton.textContent === 'Edit Profile') {
    editButton.textContent = 'Save Profile';
    hide(firstNameText);
    hide(lastNameText);
    show(firstNameInput);
    show(lastNameInput);
  } else {
    editButton.textContent = 'Edit Profile';
    hide(firstNameInput);
    hide(lastNameInput);
    show(firstNameText);
    show(lastNameText);
  }
}

function handleFirstNameChange() {
  firstNameText.textContent = firstNameInput.value;
  helloText.textContent = (
    'Hello ' +
    firstNameInput.value + ' ' +
    lastNameInput.value + '!'
  );
}

function handleLastNameChange() {
  lastNameText.textContent = lastNameInput.value;
  helloText.textContent = (
    'Hello ' +
    firstNameInput.value + ' ' +
    lastNameInput.value + '!'
  );
}

function hide(el) {
  el.style.display = 'none';
}

function show(el) {
  el.style.display = '';
}

let form = document.getElementById('form');
let editButton = document.getElementById('editButton');
let firstNameInput = document.getElementById('firstNameInput');
let firstNameText = document.getElementById('firstNameText');
let lastNameInput = document.getElementById('lastNameInput');
let lastNameText = document.getElementById('lastNameText');
let helloText = document.getElementById('helloText');
form.onsubmit = handleFormSubmit;
firstNameInput.oninput = handleFirstNameChange;
lastNameInput.oninput = handleLastNameChange;
```


<!-- 0054.part.md -->




<!-- 0055.part.md -->


``` js
{
  "hardReloadOnChange": true
}
```


<!-- 0056.part.md -->




\`\`\`html public/index.html \<form id=“form”\> \<label\> First name: \<b id=“firstNameText”\>Jane\</b\> \<input id=“firstNameInput” value=“Jane” style=“display: none”\> \</label\> \<label\> Last name: \<b id=“lastNameText”\>Jacobs\</b\> \<input id=“lastNameInput” value=“Jacobs” style=“display: none”\> \</label\> \<button type=“submit” id=“editButton”\>Edit Profile\</button\> \<p\>\<i id=“helloText”\>Hello, Jane Jacobs\!\</i\>\</p\> \</form\>


\<style\> \* { box-sizing: border-box; } body { font-family: sans-serif; margin: 20px; padding: 0; } label { display: block; margin-bottom: 20px; } \</style\>


<!-- 0057.part.md -->


```` 


Imagine React didn't exist. Can you refactor this code in a way that makes the logic less fragile and more similar to the React version? What would it look like if the state was explicit, like in React?

If you're struggling to think where to start, the stub below already has most of the structure in place. If you start here, fill in the missing logic in the `updateDOM` function. (Refer to the original code where needed.)


```js


<!-- 0058.part.md -->


let firstName = 'Jane';
let LastName = 'Jacobs';
let isEditing = false;


function handleFormSubmit(e) {
  e.preventDefault();
  setIsEditing(!isEditing);
}


function handleFirstNameChange(e) {
  setFirstName(e.target.value);
}


function handleLastNameChange(e) {
  setLastName(e.target.value);
}


function setFirstName(value) {
  firstName = value;
  updateDOM();
}


function setLastName(value) {
  lastName = value;
  updateDOM();
}


function setIsEditing(value) {
  isEditing = value;
  updateDOM();
}


function updateDOM() {
  if (isEditing) {
    editButton.textContent = 'Сохранить профиль';
    // TODO: показать входы, скрыть содержимое
  } else {
    editButton.textContent = 'Редактировать профиль';
    // TODO: скрыть входы, показать содержимое
  }
  // TODO: обновить текстовые метки
}


function hide(el) {
  el.style.display = 'none';
}


function show(el) {
  el.style.display = '';
}


let form = document.getElementById('form');
let editButton = document.getElementById('editButton');
let firstNameInput = document.getElementById('firstNameInput');
let firstNameText = document.getElementById('firstNameText');
let lastNameInput = document.getElementById('lastNameInput');
let lastNameText = document.getElementById('lastNameText');
let helloText = document.getElementById('helloText');
form.onsubmit = handleFormSubmit;
firstNameInput.oninput = handleFirstNameChange;
lastNameInput.oninput = handleLastNameChange;


<!-- 0059.part.md -->


````

``` js


<!-- 0060.part.md -->


{
  "hardReloadOnChange": true
}


<!-- 0061.part.md -->


```

\`\`\`html public/index.html \<form id=“form”\> \<label\> First name: \<b id=“firstNameText”\>Jane\</b\> \<input id=“firstNameInput” value=“Jane” style=“display: none”\> \</label\> \<label\> Last name: \<b id=“lastNameText”\>Jacobs\</b\> \<input id=“lastNameInput” value=“Jacobs” style=“display: none”\> \</label\> \<button type=“submit” id=“editButton”\>Edit Profile\</button\> \<p\>\<i id=“helloText”\>Hello, Jane Jacobs\!\</i\>\</p\> \</form\>

\<style\> \* { box-sizing: border-box; } body { font-family: sans-serif; margin: 20px; padding: 0; } label { display: block; margin-bottom: 20px; } \</style\>

```` 


<!-- 0062.part.md -->





<Решение


Отсутствующая логика включала переключение отображения входов и содержимого, а также обновление меток:


<!-- 0063.part.md -->


```js
let firstName = 'Jane';
let lastName = 'Jacobs';
let isEditing = false;

function handleFormSubmit(e) {
  e.preventDefault();
  setIsEditing(!isEditing);
}

function handleFirstNameChange(e) {
  setFirstName(e.target.value);
}

function handleLastNameChange(e) {
  setLastName(e.target.value);
}

function setFirstName(value) {
  firstName = value;
  updateDOM();
}

function setLastName(value) {
  lastName = value;
  updateDOM();
}

function setIsEditing(value) {
  isEditing = value;
  updateDOM();
}

function updateDOM() {
  if (isEditing) {
    editButton.textContent = 'Save Profile';
    hide(firstNameText);
    hide(lastNameText);
    show(firstNameInput);
    show(lastNameInput);
  } else {
    editButton.textContent = 'Edit Profile';
    hide(firstNameInput);
    hide(lastNameInput);
    show(firstNameText);
    show(lastNameText);
  }
  firstNameText.textContent = firstName;
  lastNameText.textContent = lastName;
  helloText.textContent = (
    'Hello ' +
    firstName + ' ' +
    lastName + '!'
  );
}

function hide(el) {
  el.style.display = 'none';
}

function show(el) {
  el.style.display = '';
}

let form = document.getElementById('form');
let editButton = document.getElementById('editButton');
let firstNameInput = document.getElementById('firstNameInput');
let firstNameText = document.getElementById('firstNameText');
let lastNameInput = document.getElementById('lastNameInput');
let lastNameText = document.getElementById('lastNameText');
let helloText = document.getElementById('helloText');
form.onsubmit = handleFormSubmit;
firstNameInput.oninput = handleFirstNameChange;
lastNameInput.oninput = handleLastNameChange;
````


<!-- 0064.part.md -->




<!-- 0065.part.md -->


``` js
{
  "hardReloadOnChange": true
}
```


<!-- 0066.part.md -->




\`\`\`html public/index.html \<form id=“form”\> \<label\> First name: \<b id=“firstNameText”\>Jane\</b\> \<input id=“firstNameInput” value=“Jane” style=“display: none”\> \</label\> \<label\> Last name: \<b id=“lastNameText”\>Jacobs\</b\> \<input id=“lastNameInput” value=“Jacobs” style=“display: none”\> \</label\> \<button type=“submit” id=“editButton”\>Edit Profile\</button\> \<p\>\<i id=“helloText”\>Hello, Jane Jacobs\!\</i\>\</p\> \</form\>


\<style\> \* { box-sizing: border-box; } body { font-family: sans-serif; margin: 20px; padding: 0; } label { display: block; margin-bottom: 20px; } \</style\> \`\`\`


The `updateDOM` function you wrote shows what React does under the hood when you set the state. (However, React also avoids touching the DOM for properties that have not changed since the last time they were set.)


\</Solution\>


\</Challenges\>


<!-- 0067.part.md -->


