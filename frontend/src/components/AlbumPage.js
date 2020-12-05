import React, { useState, useEffect } from 'react';
import { get_album_info } from './../server'
import AlbumOverview from './AlbumOverview'
import CircularProgress from '@material-ui/core/CircularProgress';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';

const useStyles = makeStyles(() => ({
  loadingGrid: {
    height: "80vh",
    paddingTop: "250px",
  }
}));

function AlbumPage(props) {
  const albumName = props.match.params.albumName;
  const [albumData, setAlbumData] = useState(null);
  const classes = useStyles();

  // Update the album data from server every 5 seconds
  useEffect(() => {
    get_album_info(albumName).then((data) => {
      setAlbumData(data);
    });
    const interval = setInterval(() => {
      get_album_info(albumName).then((data) => {
        setAlbumData(data);
      });
    }, 5000);
    return () => clearInterval(interval);
  }, [albumName]);

  if (!albumData) {
    return (
      <Grid container className={classes.loadingGrid} spacing={2} justify="center">
        <CircularProgress/>
      </Grid>
    )
  }

  return (
    <AlbumOverview albumData={albumData} setAlbumData={setAlbumData}/>
  );
}

export default AlbumPage
