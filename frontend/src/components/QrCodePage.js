import React from 'react';
import { get_qr_codes } from './../server';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import { makeStyles } from '@material-ui/core/styles';
import Header from './Header';

const useStyles = makeStyles((theme) => ({
  qrCodeGridItem: {
    width: "45%"
  },
  image: {
    width: "100%"
  },
  qrCodeGrid: {
    marginTop: "5%"
  }
}));

function QrCodePage() {
  const classes = useStyles();
  const [qrCodeData, setQrCodeData] = React.useState([]);
  React.useEffect(() => {
    async function fetchData() {
      const response = await get_qr_codes()
      setQrCodeData(response.qr_codes)
    }
    fetchData()
  }, []);

  const qrCodes = qrCodeData.map((qrCode, index) => (
    <Grid item key={index} className={classes.qrCodeGridItem}>
      <img className={classes.image}
           src={qrCode.url}
           alt={qrCode.name}/>
      <Typography variant="h6" align="center">
        {qrCode.information}
      </Typography>
    </Grid>
  ))

  return (
    <>
      <Header/>
      <Grid container justify="space-around" className={classes.qrCodeGrid}>
        {qrCodes}
      </Grid>
    </>
  );
}

export default QrCodePage
