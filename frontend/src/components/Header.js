import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import CameraIcon from '@material-ui/icons/PhotoCamera';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button'
import { Link } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(2),
  },
  logo: {
    textDecoration: "inherit",
    color: "inherit",
    textTransform: "none"
  }
}));

function Header() {
  const classes = useStyles();
  return (
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
  );
}

export default Header
