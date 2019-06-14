#!/usr/bin/env python3
    
from __future__ import division
from webthing import (Action, Event, Property, SingleThing, Thing, Value,
                      WebThingServer)
import logging
import time
import uuid

from tetrahedron import Tetrahedron

log = logging.getLogger(__name__)

class TetrahedronThing(Thing):

    def __init__(self, tet):
        Thing.__init__(self, 'Tetrahedron', ['OnOffSwitch', 'Light'], 'A tetrahedron shaped LED art installation.')

        self.on = False
        self.tetrahedron = tet

        self.add_property(
            Property(self,
                     'on',
                     Value(self.on, self.set_on_off),
                     metadata={
                         '@type': 'OnOffProperty',
                         'title': 'On/Off',
                         'type': 'boolean',
                         'description': 'Whether the tetrahedron is turned on',
                     }))

        
        self.add_property(
             Property(self,
                     'brightness',
                     Value(50),
                     metadata={
                         '@type': 'BrightnessProperty',
                         'title': 'Brightness',
                         'type': 'integer',
                         'description': 'The level of tetrahedron from 0-100',
                         'minimum': 0,
                         'maximum': 100,
                         'unit': 'percent',
                     }))


    def set_on_off(self, on_off):
        self.on = on_off
        self.tetrahedron.set_state(on_off)


def run_server():
    tet = Tetrahedron()
    tet.start()

    thing = TetrahedronThing(tet)
    server = WebThingServer(SingleThing(thing), port=8888)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('stopping tetrahedron')
        tet.end()
        tet.join()
        logging.info('done')



if __name__ == '__main__':
#    logging.basicConfig(
#        level=10,
#        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
#    )
#    run_server()
    tet = Tetrahedron()
    tet.run()
