import './App.css';


const baseURL = process.env.ENDPOINT || 'http://localhost:8000';


const getHelloWorld = async () => {
  console.log('clicked "Hello"')

  fetch(`${baseURL}/hello/`).then(response => {
    if (response.ok) {
      return response.json();
    }
  })
  .then(responseJson => {
    console.log(responseJson);
  })
  .catch(error => {
    console.error(error);
  })
}


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <button onClick={getHelloWorld}>
          Hello
        </button>
      </header>
    </div>
  );
}

export default App;
