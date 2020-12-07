import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import UserPages from './components/UserPages'
import LastImage from './components/LastImage'

import {
  BrowserRouter as Router,
  Route,
  Switch,
} from 'react-router-dom';


function App() {
  return (
    <>
      <CssBaseline />
      <Router>
        <Switch>
          <Route exact path='/album/:albumName/last_image' component={ LastImage }/>
          <Route path='/' component={ UserPages }/>
        </Switch>
      </Router>
    </>
  );
}

export default App;
