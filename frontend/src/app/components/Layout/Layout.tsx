import React from 'react';
import Container from '@mui/material/Container';
import Box from '@mui/material/Box';

import Navbar from './Navbar';
import Footer from './Footer';

export interface IProps {
  children?: React.JSX.Element | React.JSX.Element[] | boolean
}

const Layout = ({ children }: IProps): React.JSX.Element => {
  return (
    <>
      <Container
        maxWidth={false}
        disableGutters
      >
        <Navbar />
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'space-between',
            marginTop: 3,
            minHeight: '100vh'
          }}
        >
          <Container
            maxWidth="xl"
            sx={{
              marginBottom: 5
            }}
          >
            {children !== undefined && children}
          </Container>
          <Footer />
        </Box>
      </Container>
    </>
  );
};

export default Layout;
