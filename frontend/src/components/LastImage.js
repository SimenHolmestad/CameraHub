import React from 'react';
import { get_last_image_url } from './../server'
import CircularProgress from '@material-ui/core/CircularProgress';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles(() => ({
  image: {
    width: "100%",
    height: "100vh",
  },
  background: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height:" 100%",
    backgroundColor: "black"
  }
}));

function LastImage(props) {
  const [imageUrl, setImageUrl] = React.useState(null);
  const [albumEmpty, setAlbumEmpty] = React.useState(false);
  const [albumExists, setAlbumExists] = React.useState(true);
  const classes = useStyles();

  const getLastImageData = () => {
    get_last_image_url(albumName).then((data) => {
      if (data["error"]) {
        if (data["error"] === "album is empty") {
          setAlbumEmpty(true)
        } else {
          setAlbumExists(false)
        }
      }
      setImageUrl(data["last_image_url"]);
    });
  }

  const albumName = props.match.params.albumName;
  React.useEffect(() => {
    getLastImageData()
    const interval = setInterval(getLastImageData, 1000);
    return () => clearInterval(interval);
  }, [albumName]);

  if (!albumExists) {
    return <p>There is no album named {albumName}</p>
  }

  if (albumEmpty) {
    return <p>Album is empty</p>
  }

  if (!imageUrl) {
    return <CircularProgress/>
  }

  return (
    <div className={ classes.background }>
      <img src={imageUrl} className={ classes.image } alt=""/>
    </div>
  );
}

export default LastImage
