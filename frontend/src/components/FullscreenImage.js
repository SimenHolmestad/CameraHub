import React from 'react';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
  image: {
    maxWidth: "100%",
    maxHeight: "100%",
    bottom: "0",
    left: "0",
    margin: "auto",
    position: "fixed",
    right: "0",
    top: "0",
    objectFit: "contain",
    zoom: 10
  },
  background: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height:" 100%",
    backgroundColor: "black"
  }
}))

function FullscreenImage({ imageUrl }) {
  const classes = useStyles();
  return (
    <div className={ classes.background }>
      <img src={imageUrl} className={ classes.image } alt=""/>
    </div>
  );
}

export default FullscreenImage
