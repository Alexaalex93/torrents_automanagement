# -*- coding: utf-8 -*-
"""
Created on Sun Apr 10 12:29:44 2022

@author: AlexPC
"""

from parameterized import parameterized
import mock
import sys
import pytest

sys.path.append("../src/")

from rename_and_move import rename_and_move


@pytest.mark.parametrize('input_movie, expected_folder_output, expected_movie_output, tracker', [
                ('4 Blocks (Four Blocks) (2017) S01 [PACK][HMAX WEB-DL 1080p AVC ES-DE DD+ 5.1 Subs][HDO].mkv', '4 Blocks (Four Blocks) (2017)', '4 Blocks (Four Blocks) (2017).mkv', 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Muerte en el Nilo (2022) Hibrido [UHDRemux 2160p HEVC DV-HDR10  ES DTS 5.1 EN True-HD Atmos 7.1 Subs]HDO.mkv', 'Muerte en el Nilo (2022)', 'Muerte en el Nilo (2022).mkv', 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Rams (El valle de los carneros) (2015) [BDRemux 1080p AVC ES-ICL DTS-HD MA 5.1 Subs][HDO].mkv', 'Rams (El valle de los carneros) (2015)', 'Rams (El valle de los carneros) (2015).mkv', 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Tora! Tora! Tora! (1970) [BDRemux 1080p AVC ES DTS 5.1 - EN DTS-HD MA 5.1 Subs][lHDO].mkv', 'Tora! Tora! Tora! (1970)', 'Tora! Tora! Tora! (1970).mkv', 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Tiana y el sapo (2009) [Ángulo Castellano][UHDRemux 2160p HEVC HDR10 ES DTS 5.1 - EN TrueHD Atmos 7.1 Subs][HDO].mkv', 'Tiana y el sapo (2009)', 'Tiana y el sapo (2009).mkv', 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Bob James Trio - Feel Like Making Live! 2021 (2022) [BDRemux 1080p AVC EN True Atmos 7.1 Subs][HDO].mkv', 'Bob James Trio - Feel Like Making Live! 2021 (2022)', 'Bob James Trio - Feel Like Making Live! 2021 (2022).mkv', 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Hide and Seek (2021) BDRemux 1080p AVC ES - EN DTS-HD MA 5.1 Subs]HDO.mkv', 'Hide and Seek (2021)', 'Hide and Seek (2021).mkv', 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Eric Clapton and Steve Winwood - Live from Madison Square Garden (2009)[BDRemux AVC 1080p Ing PCM 2.0 DTS-HD MA 5.1] [HDOlimpo].mkv', 'Eric Clapton and Steve Winwood - Live from Madison Square Garden (2009)', 'Eric Clapton and Steve Winwood - Live from Madison Square Garden (2009).mkv', 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Halloween Kills (2021) V.Extendida[UHDRemux  Híbrido  2160p DV HDR10 ES DD+7.1 EN True-HD Atmos 7.1 Subs]HDO .mkv', 'Halloween Kills (2021)', 'Halloween Kills (2021).mkv', 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Umma.2022.2160p.WEB-DL.DD5.1.H.265-EVO.mkv', 'Umma (2022)', 'Umma (2022).mkv', 'https://tracker.privatehd.to/4b552343343242'),
                ('Tombo.4312.2018.1080p.AMZN.WEB-DL.DDP2.0.H.264-ZjednoczonaPrawica.mkv', 'Tombo 4312 (2018)', 'Tombo 4312 (2018).mkv', 'https://tracker.privatehd.to/4b552343343242'),
                ('Tony.Hawk.Until.the.Wheels.Fall.Off.2022.1080p.HMAX.WEB-DL.DD5.1.H.264-FLUX.mkv', 'Tony Hawk Until the Wheels Fall Off (2022)', 'Tony Hawk Until the Wheels Fall Off (2022).mkv', 'https://tracker.privatehd.to/4b552343343242'),
                ('Zack Hample vs. The World (2022) 1080p WEB-DL DD+ 5.1 H.264-STORINATOR.mkv', 'Zack Hample vs The World (2022)', 'Zack Hample vs The World (2022).mkv', 'https://tracker.privatehd.to/4b552343343242'),
                ('Zack Hample vs. The World 2022 1080p WEB-DL DD+ 5.1 H.264-STORINATOR.mkv', 'Zack Hample vs The World (2022)', 'Zack Hample vs The World (2022).mkv', 'https://tracker.privatehd.to/4b552343343242'),
                ('The.Last.Duel.2021.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HEVC.HYBRID.REMUX-FraMeSToR.mkv', 'The Last Duel (2021)', 'The Last Duel (2021).mkv', 'https://tracker.privatehd.to/4b552343343242'),
                ('Ant-Man.2015.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HEVC.HYBRID.REMUX-FraMeSToR.mkv', 'Ant-Man (2015)', 'Ant-Man (2015).mkv', 'https://tracker.privatehd.to/4b552343343242'),
                ('Hatchet.2006.Unrated.Directors.Cut.1080p.BluRay.REMUX.AVC.TrueHD.5.1-TRiToN.mkv', 'Hatchet (2006)', 'Hatchet (2006).mkv', 'https://tracker.privatehd.to/4b552343343242'),
                ('Spider-Man.3.2007.UHD.BluRay.2160p.TrueHD.Atmos.7.1.DV.HEVC.HYBRID.REMUX-FraMeSToR.mkv', 'Spider-Man 3 (2007)', 'Spider-Man 3 (2007).mkv', 'https://tracker.privatehd.to/4b552343343242')])


def test_rename_and_move_movies(input_movie, expected_folder_output, expected_movie_output, tracker, mocker):
    mock_send_message_init = mocker.patch('rename_and_move.SendMessage.__init__', return_value=None)
    mock_send_message_to_log_bot = mocker.patch('rename_and_move.SendMessage.to_log_bot', return_value='Mensaje enviado a log de bot')
    mock_os_mkdir= mocker.patch('rename_and_move.os.mkdir', return_value=None)
    mock_shutil_copy = mocker.patch('rename_and_move.shutil.copy', return_value=None)


    folder_output, movie_output = rename_and_move(tracker=tracker, source_path=f'/downloads/peliculas_4K_webdl/{input_movie}', script_path='loquesea', tmp_path='temporal_path', category='peliculas_4K_webdl', original_file_name=input_movie)
    assert folder_output == expected_folder_output
    assert movie_output == expected_movie_output


@pytest.mark.parametrize('input_serie, expected_folder_output, expected_season_episode, tracker', [
                ('ATLANTIC CROSSING 2020 S012e2 MINISERIE [PACK][M+ WEB-DL 1080P AVC ES-MUL AAC 2.0 SUBS][HDO]', 'ATLANTIC CROSSING (2020)', {'seasons':[12], 'episode':2}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Hatfields & McCoys (2012) [Miniserie][WEB-DL 1080p AVC ES DD 5.1 Subs][HDO]', 'Hatfields & McCoys (2012)', {'seasons':[], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Crímenes (2020) S02 (PACK) [M+ WEB-DL 1080p AVC ES DD 2.0 Subs][HDO]', 'Crímenes (2020)', {'seasons':[2], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('El Crimen de la Guardia Urbana [MiniSerie] [PACK] [MicroHD720 AVC ES DD 2.0]', 'El Crimen de la Guardia Urbana', {'seasons':[], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Divorce (2016) [SerieCompleta][HMAX WEB-DL 1080p AVC ES-EN DD+ 5.1 Subs][HDO]', 'Divorce (2016)', {'seasons':[], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Dragon Ball (1986) (SERIE COMPLETA) [BDRemux 1080p AVC Multiaudio DTS-HD MA 2.0 Subs][HDO]', 'Dragon Ball (1986)', {'seasons':[], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Dexter New Blood (Miniserie de TV) (2021) [BDRemux 1080p AVC ES DD 5.1 EN TrueHD 5.1 Subs][HDO]', 'Dexter New Blood (2021)', {'seasons':[], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Galáctica, estrella de combate (2004) S02 + MiniSerie [PACK][BDRip 1080p AVC ES-EN DD 2.0 Subs]', 'Galáctica, estrella de combate (2004)', {'seasons':[2], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Spartacus Dioses de la Arena (2011) [Miniserie][BDRemux 1080p AVC  ES-EN DTS-HD MA 5.1  Subs][HDO]', 'Spartacus Dioses de la Arena (2011)', {'seasons':[], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Unidad de investigación (2006) S01-S02 [PACK][M+ WEB-DL AVC 1080p AAC ES-2.0 , FR-2.0][HDO]', 'Unidad de investigación (2006)', {'seasons':[1,2], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('LEO MATTEI, BRIGADA DE MENORES (2013) S01-S02-S03 [PACK][M+ WEB-DL 1080P AVC ES-FR AAC 2.0 SUBS]', 'LEO MATTEI, BRIGADA DE MENORES (2013)', {'seasons':[1,2,3], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('RANMA 1/2 (1989) S01-02 [SERIE TV][BOX 1][FULLBLURAY 1080P AVC ES-CA-JP DTS-HD 2.0 SUBS]', 'RANMA 1/2 (1989)', {'seasons':[1,2], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('EL IMPERIO ROMANO (2016) S01-S02-S03 [PACK][NF WEB-DL 1080P AVC ES-EN DD+ 5.1 SUBS][HDO]', 'EL IMPERIO ROMANO (2016)', {'seasons':[1,2,3], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('AGALLAS EL PERRO COBARDE (1999-2002) S01-S04 [SERIE COMPLETA][CN WEB-DL 512P 43 AVC ES DD 2.0][HDO]', 'AGALLAS EL PERRO COBARDE (1999)', {'seasons':[1,4], 'episode':None}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('Promised Land (2022) - S01E08 [DSP+ WEB-DL AVC 1080p DD+ ES-5.1 , EN-5.1 Subs][HDO]', 'Promised Land (2022)', {'seasons':[1], 'episode':8}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ('S.W.A.T. Los hombres de Harrelson (2017) - S05E18 [AMZN WEB-DL AVC 1080p DD ES-2.0, EN-5.1 Subs][HDO].mkv', 'S.W.A.T. Los hombres de Harrelson (2017)', {'seasons':[5], 'episode':18}, 'https://hd-olimpo.club/announce/QlV9CdZiw4CC03yIZ09VeZTEBM9GeBZ9'),
                ])


def test_rename_and_move_series(input_serie , expected_folder_output, expected_season_episode, tracker, mocker):
    mock_send_message_init = mocker.patch('rename_and_move.SendMessage.__init__', return_value=None)
    mock_send_message_to_log_bot = mocker.patch('rename_and_move.SendMessage.to_log_bot', return_value='Mensaje enviado a log de bot')
    mock_os_mkdir= mocker.patch('rename_and_move.os.mkdir', return_value=None)
    mock_shutil_copytree = mocker.patch('rename_and_move.shutil.copytree', return_value=None)


    folder_output, season_episode_output = rename_and_move(tracker=tracker, source_path=f'/downloads/series_4K_webdl/{input_serie}', script_path='loquesea', tmp_path='temporal_path', category='series_4K_webdl', original_file_name=input_serie)
    assert folder_output == expected_folder_output
    assert season_episode_output == expected_season_episode