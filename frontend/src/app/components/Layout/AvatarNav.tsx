import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import {
  Divider,
  IconButton,
  Menu,
  MenuItem,
  Typography
} from '@mui/material';

import { useAppSelector } from '../../hooks';
import AvatarBase from './AvatarBase';

const userMenuOptions = [
  {
    name: 'Logout',
    url: '/logout'
  }
];

const Avatar = (): React.JSX.Element => {
  const navigate = useNavigate();
  const user = useAppSelector(state => state.user);
  const [anchorElUser, setAnchorElUser] = useState<null | HTMLElement>(null);

  const handleOpenUserMenu = (event: React.MouseEvent<HTMLElement>): void => {
    if (user.status !== 'loaded') {
      navigate('/login');
    }
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseUserMenu = (): void => {
    setAnchorElUser(null);
  };

  const handleNavigate = (url: string) => () => {
    handleCloseUserMenu();
    navigate(url);
  };

  return (
    <>
      <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
        <AvatarBase />
      </IconButton>
      {user.entity !== null && (
        <Menu
          sx={{
            mt: '45px'
          }}
          anchorEl={anchorElUser}
          anchorOrigin={{
            vertical: 'top',
            horizontal: 'right'
          }}
          keepMounted
          transformOrigin={{
            vertical: 'top',
            horizontal: 'right'
          }}
          open={Boolean(anchorElUser)}
          onClose={handleCloseUserMenu}
        >
          <MenuItem>
            <Typography
              textAlign="center"
              // WIP
              // onClick={handleNavigate('/profile')}
            >
              {user.entity.username}
            </Typography>
          </MenuItem>
          <Divider />
          {userMenuOptions.map(option => (
            <MenuItem
              key={option.url}
              onClick={handleNavigate(option.url)}
            >
              <Typography
                textAlign="center"
              >
                {option.name}
              </Typography>
            </MenuItem>
          ))}
        </Menu>
      )}
    </>
  );
};

export default Avatar;
