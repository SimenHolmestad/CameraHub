import React from 'react';
import { get_last_image_url } from './../server'
import CircularProgress from '@material-ui/core/CircularProgress';
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Container from '@material-ui/core/Container';

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
  },
  background: {
    position: "fixed",
    top: 0,
    left: 0,
    width: "100%",
    height:" 100%",
    backgroundColor: "black"
  },
  noImagesDiv: {
    height: "90vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center"
  }
}));

function LastImage(props) {
  const [imageUrl, setImageUrl] = React.useState(null);
  const [albumEmpty, setAlbumEmpty] = React.useState(false);
  const [albumExists, setAlbumExists] = React.useState(true);
  const classes = useStyles();
  const albumName = props.match.params.albumName;

  React.useEffect(() => {
    const getLastImageData = () => {
      get_last_image_url(albumName).then((data) => {
        if (data["error"] && data["error"] === "album is empty") {
          setAlbumEmpty(true)
        } else if (data["error"]) {
          setAlbumExists(false)
        } else {
          setImageUrl(data["last_image_url"]);
          setAlbumEmpty(false)
        }
      });
    }

    getLastImageData()
    const interval = setInterval(getLastImageData, 1500);
    return () => clearInterval(interval);
  }, [albumName]);

  if (!albumExists) {
    return <h1>There is no album named {albumName}</h1>
  }

  if (albumEmpty) {
    return (
      <div className={ classes.noImagesDiv }>
        <Container justify="center" maxWidth="sm">
          <Typography variant="h3" className={classes.emptyAlbumText} align="center" color="textSecondary" gutterBottom>
            There are no images
          </Typography>
          <Typography variant="h5" className={classes.emptyAlbumText} align="center" color="textSecondary" paragraph>
            There are currently no images in this album. The last image captured will appear here when images are captured to the album.
          </Typography>
        </Container>
      </div>
    )
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
