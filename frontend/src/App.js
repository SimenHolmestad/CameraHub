import React from 'react';
import CssBaseline from '@material-ui/core/CssBaseline';
import UserPages from './components/UserPages'
import LastImagePage from './components/LastImagePage'
import QrCodePage from './components/QrCodePage'
import QrCodeLastImagePage from './components/QrCodeLastImagePage'
import SlideshowLastImagePage from './components/SlideshowLastImagePage'
import SlideshowPage from './components/SlideshowPage'

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
          <Route exact path='/album/:albumName/last_image' component={ LastImagePage }/>
          <Route exact path='/album/:albumName/last_image_qr' component={ QrCodeLastImagePage }/>
          <Route exact path='/album/:albumName/slideshow' component={ SlideshowPage }/>
          <Route exact path='/album/:albumName/slideshow_last_image' component={ SlideshowLastImagePage }/>
          <Route exact path='/qr' component={ QrCodePage }/>
          <Route path='/' component={ UserPages }/>
        </Switch>
      </Router>
    </>
  );
}

export default App;
