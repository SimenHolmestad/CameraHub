import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import ArrowBack from '@material-ui/icons/ArrowBack';
import ArrowForward from '@material-ui/icons/ArrowForward';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Container from '@material-ui/core/Container';
import CircularProgress from '@material-ui/core/CircularProgress';
import { Link } from 'react-router-dom';

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

function ImageDetail({imageUrls, imageIndex, setImageIndex, albumName}) {
  const classes = useStyles();
  const [leftIsLoading, setLeftIsLoading] = React.useState(false);
  const [rightIsLoading, setRightIsLoading] = React.useState(false);

  const goToNextImage = () => {
    if (imageIndex > 1) {
      setImageIndex(imageIndex - 1)
      setRightIsLoading(true)
    }
  }

  const goToPreviousImage = () => {
    if (imageIndex < imageUrls.length) {
      setImageIndex(imageIndex + 1)
      setLeftIsLoading(true)
    }
  }

  const doneLoading = () => {
    setLeftIsLoading(false)
    setRightIsLoading(false)
  }

  const leftButtonDisabled = imageIndex >= imageUrls.length
  const rightButtonDisabled = imageIndex <= 1

  let leftButton = null
  if (leftIsLoading) {
    leftButton = <CircularProgress size="2em"/>
  } else {
    leftButton = (
      <Button onClick={goToPreviousImage} disabled={leftButtonDisabled}>
        <ArrowBack className={classes.leftIcon} />
        Previous image
      </Button>
    )
  }

  let rightButton = null
  if (rightIsLoading) {
    rightButton = <CircularProgress size="2em"/>
  } else {
    rightButton = (
      <Button onClick={goToNextImage} disabled={rightButtonDisabled}>
        Next image
        <ArrowForward className={classes.rightIcon} />
      </Button>
    )
  }

  return (
    <>
      <Grid container className={classes.backLinkGrid} spacing={2} justify="center">
        <Button component={Link} to={"/album/" + albumName}>
          <ArrowBack className={classes.leftIcon} />
          Back to album
        </Button>
      </Grid>
      <Container className={classes.imageContainer}>
        <img className={classes.image}
             onLoad={doneLoading}
             src={imageUrls[imageUrls.length - imageIndex]}
             alt=""/>
        <Grid container justify="space-between">
          {leftButton}
          {rightButton}
        </Grid>
      </Container>
    </>
  );
}

export default ImageDetail
