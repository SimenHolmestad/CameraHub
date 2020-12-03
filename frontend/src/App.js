import Menu from './components/Menu';
import AlbumPage from './components/AlbumPage';
import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import CameraIcon from '@material-ui/icons/PhotoCamera';
import CssBaseline from '@material-ui/core/CssBaseline';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';

import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(2),
  },
  footer: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(6),
  },
}));


function App() {
  const classes = useStyles();
  return (
    <>
      <CssBaseline />
      {/* header */}
      <AppBar position="relative">
        <Toolbar>
          <CameraIcon className={classes.icon} />
          <Typography variant="h6" color="inherit" noWrap>
            CameraHub
          </Typography>
        </Toolbar>
      </AppBar>
      {/* content */}
      <Router>
        <Switch>
          <Route exact path='/album/:albumName' component={ AlbumPage }/>
          <Route exact path='/' component={ Menu }/>
        </Switch>
      </Router>
      {/* Footer */}
      <footer className={classes.footer}>
        <Typography variant="h6" align="center" gutterBottom>
          Why are you reading this? Go take som pictures!
        </Typography>
        <Typography variant="subtitle1" align="center" color="textSecondary" component="p">
          CameraHub is made using Python, Flask, React and Material UI. The source code is openly available on <a href="https://github.com/SimenHolmestad/CameraHub" target="_blank" rel="noreferrer">GitHub</a>.
        </Typography>
      </footer>
    </>
  );
}

export default App;
