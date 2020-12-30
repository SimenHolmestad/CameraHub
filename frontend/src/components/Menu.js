import React, { useState, useEffect } from 'react';
import Card from '@material-ui/core/Card';
import { get_available_album_data } from './../server'
import NewAlbumDialog from './NewAlbumDialog';
import { Link, Redirect } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import CircularProgress from '@material-ui/core/CircularProgress';
import Grid from '@material-ui/core/Grid';

const useAlbumData = () => {
  const [albumData, setAlbumData] = useState(null);
  useEffect(() => {
    get_available_album_data().then((data) => setAlbumData(data));
  }, []);
  return albumData;
};

const useStyles = makeStyles((theme) => ({
  heroContent: {
    backgroundColor: theme.palette.background.paper,
    padding: theme.spacing(8, 0, 6),
  },
  albumCardContainer: {
    paddingBottom: "20px",
    minHeight: "50vh"
  },
  card: {
    height: '100%',
    width: '100%',
    marginTop: '20px',
    paddingTop: '10px',
    cursor: 'pointer'
  },
  albumLink: {
    textDecoration:"inherit",
    color:"inherit",
    textTransform: "none"
  },
  albumLinkText: {
    fontWeight: '200'
  },
  loadingGrid: {
    paddingTop: "30px",
    paddingBottom: "10px",
  }
}));

function Menu() {
  const albumData = useAlbumData();
  const classes = useStyles();
  const [dialogOpen, setDialogOpen] = React.useState(false);

  let albumList = null
  if (!albumData) {
    return (
      <Grid container className={classes.loadingGrid} spacing={2} justify="center">
        <CircularProgress/>
      </Grid>
    )
  } else if (albumData.forced_album) {
    return <Redirect to={"/album/" + albumData.forced_album} />
  } else {
    albumList = albumData.available_albums.map((albumName) => (
      <Link key={albumName} to={ "/album/" + albumName } className={classes.albumLink}>
        <Card className={classes.card}>
          <Typography variant="h3" align="center" color="textPrimary" className={classes.albumLinkText} paragraph>
            { albumName }
          </Typography>
        </Card>
      </Link>
    ))
  }

  const handleClickOpen = () => {
    setDialogOpen(true);
  };

  const handleClose = () => {
    setDialogOpen(false);
  };

  return (
    <>
      <div className={classes.heroContent}>
        <Container maxWidth="sm">
          <Typography component="h1" variant="h2" align="center" color="textPrimary" gutterBottom>
            Welcome to CameraHub!
          </Typography>
          <Typography variant="h5" align="center" color="textSecondary" paragraph>
            You can use CameraHub to capture images or view already captured images. Choose one of the albums below or create a new album to start!
          </Typography>
        </Container>
      </div>
      <Container maxWidth="md" className={classes.albumCardContainer}>
        { albumList }
        <Card className={classes.card} onClick={handleClickOpen}>
          <Typography variant="h3" align="center" color="textPrimary" className={classes.albumLinkText} paragraph>
            Create new album
          </Typography>
        </Card>
      </Container>
      <NewAlbumDialog open={dialogOpen} handleClose={handleClose}/>
    </>
  );
}

export default Menu;
