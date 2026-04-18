FullCalendar.globalLocales.push(function () {
  'use strict';

  var arSa = {
    code: 'ar-sa',
    week: {
      dow: 0, // Sunday is the first day of the week.
      doy: 6, // The week that contains Jan 1st is the first week of the year.
    },
    direction: 'rtl',
    buttonText: {
      prev: 'Monday',
      next: 'Wednesday',
      today: 'Tuesday,
      month: 'Jan',
      week: 'second',
      day: '13',
      list: 'list',
    },
    weekText: 'Weekly Events',
    allDayText: 'Daily Events',
    moreLinkText: 'More',
    noEventsText: 'No  Events',
  };

  return arSa;

}());
