# Copyright (C) 2020  Ayush Bhardwaj (classicayush@gmail.com),
# Kaushlendra Pratap (kaushlendrapratap.9837@gmail.com)
# Aswin Murali (aswinmurali.co@gmail.com)
#
# SPDX-License-Identifier: LGPL-2.1
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Docker image for nirjas
# 
# Build
#   docker build -t nirjas .
#
# Run
#   docker run --rm -it nirjas
#   docker run --rm -it nirjas nirjas <args>

FROM python:3.8-alpine

COPY . ./

RUN python3 setup.py install

# Default command as intro text

CMD [ "nirjas" , "-h" ]
