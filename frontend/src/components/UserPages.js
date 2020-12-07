import React from 'react';
import Menu from './Menu';
import AlbumPage from './AlbumPage';
import Button from '@material-ui/core/Button'
import AppBar from '@material-ui/core/AppBar';
import CameraIcon from '@material-ui/icons/PhotoCamera';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import {
  Route,
  Switch,
  Link
} from 'react-router-dom';

const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(2),
  },
  footer: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(6),
  },
  logo: {
    textDecoration:"inherit",
    color:"inherit",
    textTransform: "none"
  }
}));

function UserPages() {
  const classes = useStyles();
  return (
    <>
      {/* header */}
      <AppBar position="relative">
        <Toolbar>
          <Button component={Link} to={ "/" } className={classes.logo}>
            <CameraIcon className={classes.icon} />
            <Typography variant="h6" color="inherit" noWrap>
              CameraHub
            </Typography>
          </Button>
        </Toolbar>
      </AppBar>
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
