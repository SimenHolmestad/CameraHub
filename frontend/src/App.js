import Menu from './components/Menu';
import AlbumPage from './components/AlbumPage';
import './App.css';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        {/* <Menu/> */}
        <Router>
          <Switch>
            <Route exact path='/album/:albumName' component={ AlbumPage }/>
            <Route exact path='/' component={ Menu }/>
          </Switch>
        </Router>
      </header>
    </div>
  );
}

export default App;
