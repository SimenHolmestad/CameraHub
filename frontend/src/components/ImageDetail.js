import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import ArrowBack from '@material-ui/icons/ArrowBack';
import ArrowForward from '@material-ui/icons/ArrowForward';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';

const useStyles = makeStyles((theme) => ({
  leftIcon: {
    marginRight: theme.spacing(1),
  },
  rightIcon: {
    marginLeft: theme.spacing(1),
  },
  image: {
    width: "100%"
  },
  backLinkGrid: {
    paddingTop: "20px",
    paddingBottom: "20px",
  },
  imageContainer: {
    maxWidth: "1100px",
    padding: theme.spacing(0, 0, 0),
  },
}));

function ImageDetail({imageUrls, imageIndex, setImageIndex}) {
  const classes = useStyles();

  const goToNextImage = () => {
    if (imageIndex > 1) {
      setImageIndex(imageIndex - 1)
    }
  }

  const goToPreviousImage = () => {
    if (imageIndex < imageUrls.length) {
      setImageIndex(imageIndex + 1)
    }
  }

  const leftButtonDisabled = imageIndex >= imageUrls.length
  const rightButtonDisabled = imageIndex <= 1

  return (
    <>
      <Grid container className={classes.backLinkGrid} spacing={2} justify="center">
        <Button onClick={() => (setImageIndex(-1))}>
          <ArrowBack className={classes.leftIcon} />
          Back to album
        </Button>
      </Grid>
      <Container className={classes.imageContainer}>
        <img className={classes.image}
             src={imageUrls[imageUrls.length - imageIndex]}
             alt=""/>
        <Grid container justify="space-between">
          <Button onClick={goToPreviousImage} disabled={leftButtonDisabled}>
            <ArrowBack className={classes.leftIcon} />
            Previous image
          </Button>
          <Button onClick={goToNextImage} disabled={rightButtonDisabled}>
            Next image
            <ArrowForward className={classes.rightIcon} />
          </Button>
        </Grid>
      </Container>
    </>
  );
}

export default ImageDetail
