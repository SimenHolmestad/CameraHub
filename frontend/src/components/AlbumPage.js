import React, { useState, useEffect } from 'react';
import { get_album_info } from './../server'
import AlbumOverview from './AlbumOverview'
import ImageDetail from './ImageDetail'
import CircularProgress from '@material-ui/core/CircularProgress';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import { Route, Switch } from 'react-router-dom';

const useStyles = makeStyles(() => ({
  loadingGrid: {
    height: "80vh",
    paddingTop: "250px",
  }
}));

function AlbumPage(props) {
  const albumName = props.match.params.albumName;
  const [albumData, setAlbumData] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [imageIndex, setImageIndex] = React.useState(1);
  const info_gather_interval = React.useRef(null)
  const classes = useStyles();

  // Update the album data from server every 5 seconds
  useEffect(() => {
    const gather_album_data = async () => {
      console.log("here");
      const albumInfo = await get_album_info(albumName)
      if (albumInfo.error) {
        setErrorMessage(albumInfo.error)
        clearInterval(info_gather_interval.current)
      } else {
        setAlbumData(albumInfo);
      }
    }

    gather_album_data()
    info_gather_interval.current = setInterval(gather_album_data, 5000);
    return () => clearInterval(info_gather_interval.current);
  }, [albumName]);

  if (errorMessage) {
    return <h1>ERROR: {errorMessage}</h1>
  }

  if (!albumData) {
    return (
      <Grid container className={classes.loadingGrid} spacing={2} justify="center">
        <CircularProgress/>
      </Grid>
    )
  }

  const imageDetail = () => (
    <ImageDetail
      imageUrls={albumData.image_urls}
      imageIndex={imageIndex}
      setImageIndex={setImageIndex}
      albumName={albumName}/>
  )

  const albumOverview = () => (
    <AlbumOverview
      albumData={albumData}
      setAlbumData={setAlbumData}
      setImageIndex={setImageIndex}/>
  );

  return (
    <Switch>
      <Route exact path={`${props.match.url}/detail`} render={imageDetail} />
      <Route path={`${props.match.url}`} render={albumOverview} />
    </Switch>
  )
}

export default AlbumPage
