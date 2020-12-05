import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import ArrowBack from '@material-ui/icons/ArrowBack';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';

const useStyles = makeStyles((theme) => ({
  icon: {
    marginRight: theme.spacing(1),
  },
  image: {
    width: "100%"
  },
  backLinkGrid: {
    paddingTop: "30px",
    paddingBottom: "30px",
  },
  imageContainer: {
    maxWidth: "1200px",
    padding: theme.spacing(0, 0, 0),
  },
}));

function ImageDetail({imageUrls, imageIndex, setImageIndex}) {
  const classes = useStyles();
  return (
    <>
      <Grid container className={classes.backLinkGrid} spacing={2} justify="center">
        <Button onClick={() => (setImageIndex(-1))}>
          <ArrowBack className={classes.icon} />
          Back to album
        </Button>
      </Grid>
      <Container className={classes.imageContainer}>
        <img className={classes.image}
             src={imageUrls[imageUrls.length - imageIndex]}
             alt=""/>
      </Container>
    </>
  );
}

export default ImageDetail
