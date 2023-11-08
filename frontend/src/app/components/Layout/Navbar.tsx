import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { useTheme } from '@mui/material/styles';
import {
  AppBar,
  Box,
  Button,
  Container,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Toolbar,
  Typography
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

import Avatar from './AvatarNav';

const pages = [
  {
    name: 'My Decks',
    url: '/decks'
  }
];

const Navbar = (): React.JSX.Element => {
  const navigate = useNavigate();
  const theme = useTheme();
  const [showNavMenu, setShowNavMenu] = useState<boolean>(false);

  const toggleNavMenu = (value: boolean) => () => {
    setShowNavMenu(value);
  };

  const handleNavMenuNavigate = (url: string) => () => {
    setShowNavMenu(false);
    setTimeout(() => {
      navigate(url);
    }, theme.transitions.duration.leavingScreen);
  };

  return (
    <AppBar position="static">
      <Container disableGutters maxWidth={false}>
        <Toolbar
          sx={{
            display: 'flex',
            justifyContent: 'space-between'
          }}
        >
          <Box sx={{ flexGrow: 0, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              onClick={toggleNavMenu(true)}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Drawer
              anchor="left"
              open={showNavMenu}
              onClose={toggleNavMenu(false)}
            >
              <Box
                sx={{
                  width: 250
                }}
                role="presentation"
                onClick={toggleNavMenu(false)}
                onKeyDown={toggleNavMenu(false)}
              >
                <List>
                  {pages.map(page => (
                    <ListItem key={page.url} disablePadding>
                      <ListItemButton onClick={handleNavMenuNavigate(page.url)}>
                        <ListItemText primary={page.name} />
                      </ListItemButton>
                    </ListItem>
                  ))}
                </List>
              </Box>
            </Drawer>
          </Box>

          <Box sx={{ display: 'flex' }}>
            <Button
              onClick={() => { navigate('/'); }}
              sx={{ color: 'white' }}
            >
              <Typography
                variant="h6"
                sx={{
                  fontFamily: 'monospace',
                  fontWeight: 700
                }}
              >
                CardMaster
              </Typography>
            </Button>

            <Box sx={{
              display: { xs: 'none', md: 'flex' }
            }}>
              {pages.map(page => (
                <Button
                  key={page.url}
                  onClick={() => { navigate(page.url); }}
                  sx={{ color: 'white', display: 'block' }}
                >
                  {page.name}
                </Button>
              ))}
            </Box>
          </Box>

          <Box sx={{ flexGrow: 0 }}>
            <Avatar />
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;
