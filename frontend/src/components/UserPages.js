import React from 'react';
import Menu from './Menu';
import AlbumPage from './AlbumPage';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Header from './Header';
import {
  Route,
  Switch
} from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  footer: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(6),
  }
}));

function UserPages() {
  const classes = useStyles();
  return (
    <>
      <Header/>
      {/* content */}
      <Switch>
        <Route path='/album/:albumName' component={ AlbumPage }/>
        <Route exact path='/' component={ Menu }/>
      </Switch>
      {/* Footer */}
      <footer className={classes.footer}>
        <Typography variant="h6" align="center" gutterBottom>
          Hope you like CameraHub!
        </Typography>
        <Typography variant="subtitle1" align="center" color="textSecondary" component="p">
          CameraHub is made using Python, Flask, React and Material UI. The source code is openly available on <a href="https://github.com/SimenHolmestad/CameraHub" target="_blank" rel="noreferrer">GitHub</a>.
        </Typography>
      </footer>
    </>
  );
}

export default UserPages
