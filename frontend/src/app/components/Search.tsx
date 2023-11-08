import React from 'react';

import { styled } from '@mui/material/styles';
import {
  IconButton,
  InputBase
} from '@mui/material';

import SearchIcon from '@mui/icons-material/Search';
import ClearIcon from '@mui/icons-material/Clear';

import type { UseField } from '../hooks';

const SearchWrapper = styled('div')(() => ({
  position: 'relative',
  width: '100%'
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
  padding: theme.spacing(0, 1),
  height: '100%',
  position: 'absolute',
  pointerEvents: 'none',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center'
}));

const ClearIconWrapper = styled(IconButton)(() => ({
  position: 'absolute',
  right: 0
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  width: '100%',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    paddingRight: `calc(1em + ${theme.spacing(4)})`,
    width: '100%'
  }
}));

interface SearchProps {
  searchField: UseField
  style?: React.CSSProperties
}

const Search = ({ searchField, style }: SearchProps): React.JSX.Element => {
  const { helperText: _, ...props } = searchField.inputProps;

  return (
    <SearchWrapper style={style}>
      <SearchIconWrapper>
        <SearchIcon />
      </SearchIconWrapper>
      <StyledInputBase
        placeholder="Search…"
        {...props}
      />
      {searchField.value.length > 0 && (
        <ClearIconWrapper
          onClick={searchField.clear}
        >
          <ClearIcon />
        </ClearIconWrapper>
      )}
    </SearchWrapper>
  );
};

export default Search;
