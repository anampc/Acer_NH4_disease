def get_values(*names):
    import json
    #_all_values = json.loads("""{"p300mnt":"left","p20mnt":"right","mag_mod":"magnetic module","num_samples":96,"s_vol":25}""")
    _all_values = json.loads("""{"p300mnt":"left","mag_mod":"magnetic module","num_samples":96,"s_vol":25}""")# remove p20mnt?
    return [_all_values[n] for n in names]


import math

metadata = {
    'protocolName': 'PCR Clean-Up for Illumina 16S',
    'author': 'Chaz <chaz@opentrons.com>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.7'
}


def run(protocol):
#[p300mnt, p20mnt, mag_mod, num_samples, s_vol] = get_values(  # noqa: F821
   # 'p300mnt', 'p20mnt', 'mag_mod', 'num_samples', 's_vol')
    [p300mnt, mag_mod, num_samples, s_vol] = get_values(  # noqa: F821
    'p300mnt', 'mag_mod', 'num_samples', 's_vol')

    # load labware and pipette
    #magDeck = protocol.load_module(mag_mod, '10')
    magDeck = protocol.load_module(mag_mod, '2') # Makes the plate more accessible for manual aspiration after 2nd ETOH
    magPlate = magDeck.load_labware('nest_96_wellplate_100ul_pcr_full_skirt')

    #res = protocol.load_labware('nest_12_reservoir_15ml', '7')
    res = protocol.load_labware('nest_12_reservoir_15ml', '5')

    end = protocol.load_labware('nest_96_wellplate_100ul_pcr_full_skirt', '1')

    #tips20 = [protocol.load_labware('opentrons_96_filtertiprack_20ul', '4')]

    #all_tips = [
    #    protocol.load_labware(
    #        'opentrons_96_filtertiprack_200ul', s).rows()[0] for s in [
    #            '8', '9', '5', '6', '2', '3']
            
    #Changed tips location to allow easy access to plate (place sample plate in 2 and move p300 tips to 4 that were p20 tips before)
    all_tips = [ 
        protocol.load_labware(
            'opentrons_96_filtertiprack_200ul', s).rows()[0] for s in [
                '4', '6', '7', '8', '9', '11']
                ]
    flat_tips = [tips for rack in all_tips for tips in rack]

    #m20 = protocol.load_instrument('p20_multi_gen2', p20mnt, tip_racks=tips20)
    m300 = protocol.load_instrument('p300_multi_gen2', p300mnt)

    # variable declarations
    #waste = protocol.load_labware('nest_1_reservoir_195ml', '11')['A1']
    waste = protocol.load_labware('nest_1_reservoir_195ml', '3')['A1']
    num_cols = math.ceil(num_samples/8)
    tips1, tips2, tips3, tips4, tips5, tips6 = [
        flat_tips[i:i+num_cols] for i in range(0, num_cols*6, num_cols)
        ]
    magSamps = magPlate.rows()[0][:num_cols]
    elutes = end.rows()[0][:num_cols]
    beads = res['A1']
    etoh1 = [res['A2']]*6+[res['A3']]*6
    etoh2 = [res['A4']]*6+[res['A5']]*6
    tris = res['A6']

    m300.flow_rate.aspirate = 100
    m300.flow_rate.dispense = 100
    m300.flow_rate.blow_out = 200

    def supernatant(vol, tips, utips, rtips=False):
        m300.flow_rate.aspirate = 50
        for well, tip, utip in zip(magSamps, tips, utips):
            m300.pick_up_tip(tip)
            m300.aspirate(vol, well)
            m300.dispense(vol, waste)
            m300.blow_out()
            if rtips:
                m300.drop_tip(utip)
            else:
                m300.drop_tip()
        m300.flow_rate.aspirate = 100

    magDeck.disengage()

    init_vol = 25 + s_vol
    # Add 25uL of beads
    protocol.comment('Adding 20uL of beads to wells...')
    for well, tip in zip(magSamps, tips1):
        m300.pick_up_tip(tip)
        m300.mix(5, 150, beads) # Mix beads before?
        m300.aspirate(25, beads)
        m300.dispense(25, well)
        m300.mix(10, init_vol)
        m300.blow_out()
        m300.drop_tip()

    protocol.comment('Incubating at room temp for 5 minutes...')
    protocol.delay(minutes=5)
    magDeck.engage()
    protocol.comment('Incubating for 2 minutes with MagDeck engaged...')
    protocol.delay(minutes=2)

    protocol.comment('Removing supernatant...')
    supernatant(init_vol, tips2, tips1)
    magDeck.disengage()

    # Ethanol Wash 1
    protocol.comment('Adding 195uL ethanol for wash 1...')
    for well, etoh, tip, utip in zip(magSamps, etoh1, tips3, tips2):
        m300.pick_up_tip(tip)
        m300.aspirate(195, etoh)
        m300.dispense(195, well)
        m300.blow_out()
        m300.drop_tip(utip)

    magDeck.engage()
    protocol.delay(seconds=30)

    protocol.comment('Removing supernatant...')
    supernatant(195, tips2, tips1, True)
    magDeck.disengage()

    # Ethanol Wash 2
    protocol.comment('Adding 195uL ethanol for wash 2...')
    for well, etoh, tip, utip in zip(magSamps, etoh2, tips4, tips3):
        m300.pick_up_tip(tip)
        m300.aspirate(195, etoh)
        m300.dispense(195, well)
        m300.blow_out()
        m300.drop_tip(utip)

    magDeck.engage()
    protocol.delay(seconds=30)

    protocol.comment('Removing supernatant...')
    #supernatant(195, tips3, tips2, True)
    supernatant(215, tips3, tips2, True) # Remove more volume to decrease excess ethanol and skip p20 step

    # Removing any excess ethanol with P20-Multi
    #m20.transfer(20, magSamps, waste, new_tip='always')
    #magDeck.disengage() # Protocol says airdry in magnetic stand...

    protocol.comment('Air drying for 10 minutes...')
    #protocol.delay(minutes=10)
    protocol.delay(minutes=15) # Add estra 5 min to dry more?
    magDeck.disengage() # Protocol says airdry in magnetic stand...

    protocol.comment('Adding Tris/water to samples...')
    for well, tip, utip in zip(magSamps, tips5, tips3):
        m300.pick_up_tip(tip)
        m300.aspirate(30, tris)
        m300.dispense(30, well)
        #m300.mix(5, 30)
        m300.mix(10, 30) # Says 10 times in protocol
        m300.blow_out()
        m300.drop_tip(utip)

    protocol.comment('Incubating for 2 minutes...')
    protocol.delay(minutes=2)
    magDeck.engage()
    protocol.comment('Incubating for 2 minutes with MagDeck engaged...')
    protocol.delay(minutes=2)

    m300.flow_rate.aspirate = 25
    protocol.comment('Transferring elutes to clean PCR plate in slot 1...')
    for src, dest, tip, utip in zip(magSamps, elutes, tips6, tips4):
        m300.pick_up_tip(tip)
        m300.aspirate(25, src)
        m300.dispense(25, dest)
        m300.blow_out()
        m300.drop_tip(utip)

    protocol.comment('Protocol complete!')